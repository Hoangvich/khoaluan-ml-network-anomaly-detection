"""model_adapter.py — Bộ nạp mô hình THỐNG NHẤT cho Backend.

Giải quyết 4 vấn đề tích hợp giữa hai hệ thống đóng gói (Danh vs Hoàng):
  1. Thứ tự nhãn (Label ID) khác nhau
  2. Số đặc trưng đầu vào khác nhau (56/59/62)
  3. Key trong file .joblib đặt tên khác nhau
  4. Luật quyết định (threshold vs argmax) khác nhau

Backend chỉ cần:
    adapter = ModelAdapter.load("ml_engine/LGBM/models/lgbm_F_NOOS.joblib")
    result  = adapter.predict(df_raw)
"""

import json
import time
import warnings
from pathlib import Path
from typing import Optional, Union

import joblib
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Bảng đổi tên cột từ CICFlowMeter v4 (kiểu 2018) sang tên chuẩn (2017).
# Backend nhận flow từ CICFlowMeter, luôn cần bước này.
# ---------------------------------------------------------------------------
RENAME_2018 = {
    'ACK Flag Cnt': 'ACK Flag Count', 'Bwd Blk Rate Avg': 'Bwd Avg Bulk Rate',
    'Bwd Byts/b Avg': 'Bwd Avg Bytes/Bulk', 'Bwd Header Len': 'Bwd Header Length',
    'Bwd IAT Tot': 'Bwd IAT Total', 'Bwd Pkt Len Max': 'Bwd Packet Length Max',
    'Bwd Pkt Len Mean': 'Bwd Packet Length Mean', 'Bwd Pkt Len Min': 'Bwd Packet Length Min',
    'Bwd Pkt Len Std': 'Bwd Packet Length Std', 'Bwd Pkts/b Avg': 'Bwd Avg Packets/Bulk',
    'Bwd Pkts/s': 'Bwd Packets/s', 'Bwd Seg Size Avg': 'Avg Bwd Segment Size',
    'Dst Port': 'Destination Port', 'ECE Flag Cnt': 'ECE Flag Count',
    'FIN Flag Cnt': 'FIN Flag Count', 'Flow Byts/s': 'Flow Bytes/s',
    'Flow Pkts/s': 'Flow Packets/s', 'Fwd Act Data Pkts': 'act_data_pkt_fwd',
    'Fwd Blk Rate Avg': 'Fwd Avg Bulk Rate', 'Fwd Byts/b Avg': 'Fwd Avg Bytes/Bulk',
    'Fwd Header Len': 'Fwd Header Length', 'Fwd IAT Tot': 'Fwd IAT Total',
    'Fwd Pkt Len Max': 'Fwd Packet Length Max', 'Fwd Pkt Len Mean': 'Fwd Packet Length Mean',
    'Fwd Pkt Len Min': 'Fwd Packet Length Min', 'Fwd Pkt Len Std': 'Fwd Packet Length Std',
    'Fwd Pkts/b Avg': 'Fwd Avg Packets/Bulk', 'Fwd Pkts/s': 'Fwd Packets/s',
    'Fwd Seg Size Avg': 'Avg Fwd Segment Size', 'Fwd Seg Size Min': 'min_seg_size_forward',
    'Init Bwd Win Byts': 'Init_Win_bytes_backward', 'Init Fwd Win Byts': 'Init_Win_bytes_forward',
    'PSH Flag Cnt': 'PSH Flag Count', 'Pkt Len Max': 'Max Packet Length',
    'Pkt Len Mean': 'Packet Length Mean', 'Pkt Len Min': 'Min Packet Length',
    'Pkt Len Std': 'Packet Length Std', 'Pkt Len Var': 'Packet Length Variance',
    'Pkt Size Avg': 'Average Packet Size', 'RST Flag Cnt': 'RST Flag Count',
    'SYN Flag Cnt': 'SYN Flag Count', 'Subflow Bwd Byts': 'Subflow Bwd Bytes',
    'Subflow Bwd Pkts': 'Subflow Bwd Packets', 'Subflow Fwd Byts': 'Subflow Fwd Bytes',
    'Subflow Fwd Pkts': 'Subflow Fwd Packets', 'Tot Bwd Pkts': 'Total Backward Packets',
    'Tot Fwd Pkts': 'Total Fwd Packets', 'TotLen Bwd Pkts': 'Total Length of Bwd Packets',
    'TotLen Fwd Pkts': 'Total Length of Fwd Packets', 'URG Flag Cnt': 'URG Flag Count',
}

# Nhãn chuẩn chung cho toàn bộ hệ thống (thứ tự cố định)
CANONICAL_CLASSES = ['BENIGN', 'BruteForce', 'DoS/DDoS', 'PortScan']


def _port_class(port_series: pd.Series) -> np.ndarray:
    """Phân nhóm cổng: 0=system(<1024), 1=registered(1024-49151), 2=ephemeral(≥49152)."""
    p = pd.to_numeric(port_series, errors='coerce').to_numpy(np.float64)
    out = np.where(p < 1024, 0.0, np.where(p < 49152, 1.0, 2.0))
    out[np.isnan(p)] = np.nan
    return out


def _canonicalize(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Chuẩn hoá tên cột và tạo dst_port_class nếu chưa có."""
    df = df_raw.rename(columns=lambda c: str(c).strip()).rename(columns=RENAME_2018)
    if 'dst_port_class' not in df.columns and 'Destination Port' in df.columns:
        df['dst_port_class'] = _port_class(df['Destination Port'])
    return df


class ModelAdapter:
    """Interface thống nhất cho mọi mô hình ML trong dự án.

    Attributes:
        model:        Đối tượng sklearn/xgboost/lightgbm có predict_proba().
        model_name:   Tên mô hình ("RandomForest", "LightGBM", "XGBoost", "MLP").
        features:     Danh sách đặc trưng đầu vào theo đúng thứ tự.
        classes:      Danh sách tên nhãn theo thứ tự nội bộ của mô hình.
        threshold:    Ngưỡng quyết định (None = argmax).
        benign_index: Vị trí lớp BENIGN trong mảng classes.
        is_pipeline:  True nếu model là sklearn.Pipeline (MLP cần scaler).
        format:       "danh" hoặc "hoang" — cách đóng gói gốc.
    """

    def __init__(self, model, model_name: str, features: list, classes: list,
                 threshold: Optional[float], benign_index: int,
                 is_pipeline: bool, format_type: str, metadata: dict):
        self.model = model
        self.model_name = model_name
        self.features = features
        self.classes = classes
        self.threshold = threshold
        self.benign_index = benign_index
        self.is_pipeline = is_pipeline
        self.format = format_type
        self.metadata = metadata

        # Bảng chuyển đổi nhãn: index nội bộ → tên nhãn chuẩn
        self._idx_to_name = {i: c for i, c in enumerate(classes)}
        # Bảng chuyển đổi: tên nhãn chuẩn → index nội bộ
        self._name_to_idx = {c: i for i, c in enumerate(classes)}

    # -----------------------------------------------------------------
    # NẠP MÔ HÌNH
    # -----------------------------------------------------------------
    @classmethod
    def load(cls, path: Union[str, Path]) -> 'ModelAdapter':
        """Nạp bất kỳ file .joblib nào trong dự án, tự detect format."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy: {path}")

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            pkg = joblib.load(path)

        # ---- Detect format dựa trên key ----
        if 'features' in pkg and 'classes' in pkg:
            # Format Danh: bundle có key 'features', 'classes', 'threshold'
            return cls._from_danh(pkg, path)
        elif 'feature_cols' in pkg:
            # Format Hoàng: package có key 'feature_cols', 'class_names'
            return cls._from_hoang(pkg, path)
        else:
            raise ValueError(f"Không nhận ra format đóng gói: keys = {list(pkg.keys())}")

    @classmethod
    def _from_danh(cls, pkg: dict, path: Path) -> 'ModelAdapter':
        """Parse format đóng gói của Danh (RF, LightGBM)."""
        return cls(
            model=pkg['model'],
            model_name=pkg.get('model_name', path.stem),
            features=pkg['features'],
            classes=pkg['classes'],
            threshold=pkg.get('threshold'),
            benign_index=pkg.get('benign_index', 0),
            is_pipeline=False,
            format_type='danh',
            metadata={k: v for k, v in pkg.items() if k != 'model'},
        )

    @classmethod
    def _from_hoang(cls, pkg: dict, path: Path) -> 'ModelAdapter':
        """Parse format đóng gói của Hoàng (XGBoost, MLP)."""
        if 'pipeline' in pkg:
            model = pkg['pipeline']
            is_pipeline = True
            model_name = 'MLP'
        else:
            model = pkg['model']
            is_pipeline = False
            model_name = 'XGBoost'

        classes = pkg.get('class_names', CANONICAL_CLASSES)
        return cls(
            model=model,
            model_name=model_name,
            features=pkg['feature_cols'],
            classes=classes,
            threshold=None,  # Hoàng không dùng threshold
            benign_index=classes.index('BENIGN'),
            is_pipeline=is_pipeline,
            format_type='hoang',
            metadata={k: v for k, v in pkg.items()
                      if k not in ('model', 'pipeline')},
        )

    # -----------------------------------------------------------------
    # TIỀN XỬ LÝ
    # -----------------------------------------------------------------
    def prepare(self, df_raw: pd.DataFrame):
        """Chuẩn hoá DataFrame thô → (X, valid_mask).

        Returns:
            X:     ndarray float32 hoặc DataFrame (nếu pipeline) đúng thứ tự features.
            valid: boolean mask — dòng nào hợp lệ để đưa vào model.
        """
        df = _canonicalize(df_raw)

        missing = [c for c in self.features if c not in df.columns]
        if missing:
            raise KeyError(f"Thiếu {len(missing)} cột: {missing}")

        if self.is_pipeline:
            # MLP pipeline cần DataFrame (vì scaler bên trong)
            X_df = df[self.features].apply(pd.to_numeric, errors='coerce')
            valid = X_df.notna().all(axis=1).to_numpy()
            if 'Flow Duration' in df.columns:
                dur = pd.to_numeric(df['Flow Duration'], errors='coerce').to_numpy()
                valid &= (dur > 0)
            return X_df, valid
        else:
            X = df[self.features].apply(pd.to_numeric, errors='coerce').to_numpy(np.float32)
            valid = np.isfinite(X).all(axis=1)
            if 'Flow Duration' in df.columns:
                dur = pd.to_numeric(df['Flow Duration'], errors='coerce').to_numpy()
                valid &= (dur > 0)
            return X, valid

    # -----------------------------------------------------------------
    # SUY LUẬN
    # -----------------------------------------------------------------
    def predict(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """Hàm duy nhất Backend cần gọi.

        Nhận DataFrame thô (từ CICFlowMeter hoặc pcap_to_flow), trả về DataFrame:
            - valid:        bool — dòng có hợp lệ không
            - label:        str  — tên nhãn dự đoán ("BENIGN", "DoS/DDoS", ...)
            - attack_score: float — xác suất tấn công (1 - P(BENIGN))
            - confidence:   float — xác suất của lớp được chọn
            - latency_ms:   float — thời gian suy luận
        """
        X, valid = self.prepare(df_raw)
        n = len(df_raw)

        out = pd.DataFrame({
            'valid': valid,
            'label': pd.array([''] * n, dtype='string'),
            'attack_score': np.full(n, np.nan, dtype=np.float32),
            'confidence': np.full(n, np.nan, dtype=np.float32),
        })

        if not valid.any():
            return out

        # Lấy dữ liệu hợp lệ
        X_valid = X[valid] if isinstance(X, np.ndarray) else X.loc[valid]

        # Đo latency
        t0 = time.perf_counter()
        raw_proba = self.model.predict_proba(X_valid)
        latency = (time.perf_counter() - t0) * 1000

        # Chuẩn hoá proba → luôn có đủ K cột theo đúng thứ tự self.classes
        K = len(self.classes)
        if raw_proba.shape[1] == K:
            proba = raw_proba.astype(np.float32)
        else:
            # Model chỉ trả proba cho một phần classes (hiếm gặp)
            proba = np.zeros((len(X_valid), K), dtype=np.float32)
            if hasattr(self.model, 'classes_'):
                proba[:, self.model.classes_] = raw_proba
            else:
                proba[:, :raw_proba.shape[1]] = raw_proba

        # Áp dụng luật quyết định
        if self.threshold is not None:
            # Luật threshold (Danh): tấn công nếu 1 - P(BENIGN) >= threshold
            attack_proba = proba.copy()
            attack_proba[:, self.benign_index] = -1.0
            pred_idx = np.where(
                1.0 - proba[:, self.benign_index] >= self.threshold,
                attack_proba.argmax(axis=1),
                self.benign_index
            )
        else:
            # Luật argmax (Hoàng)
            pred_idx = proba.argmax(axis=1)

        # Chuyển index → tên nhãn
        pred_labels = np.array(self.classes, dtype=object)[pred_idx]

        # Attack score = 1 - P(BENIGN)
        attack_scores = 1.0 - proba[:, self.benign_index]

        # Confidence = xác suất của lớp được chọn
        confidence = proba[np.arange(len(pred_idx)), pred_idx]

        # Ghi kết quả
        out.loc[valid, 'label'] = pred_labels
        out.loc[valid, 'attack_score'] = attack_scores
        out.loc[valid, 'confidence'] = confidence

        return out

    # -----------------------------------------------------------------
    # TIỆN ÍCH
    # -----------------------------------------------------------------
    def predict_batch_json(self, df_raw: pd.DataFrame) -> list[dict]:
        """Trả kết quả dạng list[dict] cho REST API."""
        result = self.predict(df_raw)
        records = []
        for i, row in result.iterrows():
            records.append({
                'index': int(i),
                'valid': bool(row['valid']),
                'prediction': row['label'] if row['valid'] else None,
                'is_anomaly': row['label'] != 'BENIGN' if row['valid'] else None,
                'attack_score': round(float(row['attack_score']), 4) if row['valid'] else None,
                'confidence': round(float(row['confidence']), 4) if row['valid'] else None,
            })
        return records

    def info(self) -> dict:
        """Thông tin mô hình cho API endpoint /model/info."""
        return {
            'model_name': self.model_name,
            'format': self.format,
            'n_features': len(self.features),
            'features': self.features,
            'classes': self.classes,
            'threshold': self.threshold,
            'is_pipeline': self.is_pipeline,
        }

    def __repr__(self):
        return (f"ModelAdapter(name={self.model_name!r}, format={self.format!r}, "
                f"features={len(self.features)}, classes={self.classes}, "
                f"threshold={self.threshold})")
