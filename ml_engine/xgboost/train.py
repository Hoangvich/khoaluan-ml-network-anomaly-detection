import os
import sys
import time
import argparse
import joblib
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đưa project root vào sys.path để import được data_loader và eval_utils
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import xgboost as xgb
from sklearn.utils.class_weight import compute_sample_weight

from ml_engine.data_loader import get_train_val_test_split, CLASS_NAMES
from ml_engine.eval_utils import evaluate_predictions, measure_inference_latency, format_markdown_report

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def train_xgboost(sample_ratio=None, n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42):
    print("=" * 60)
    print(f"BẮT ĐẦU HUẤN LUYỆN XGBOOST (Sample ratio: {sample_ratio if sample_ratio else '100% full dataset'})")
    print("=" * 60)
    
    # 1. Nạp và chia dữ liệu chống rò rỉ
    start_load = time.time()
    parquet_path = os.path.join(PROJECT_ROOT, "data", "processed", "unified.parquet")
    X_train, y_train, X_val, y_val, X_test, y_test, feature_cols = get_train_val_test_split(
        parquet_path=parquet_path,
        sample_ratio=sample_ratio,
        random_state=random_state
    )
    print(f"-> Nạp dữ liệu hoàn tất trong {time.time() - start_load:.1f}s")
    print(f"-> Kích thước Train: {X_train.shape[0]:,} dòng | Val: {X_val.shape[0]:,} dòng | Test: {X_test.shape[0]:,} dòng")
    print(f"-> Số lượng đặc trưng: {len(feature_cols)}")
    
    # 2. Tính sample_weight để cân bằng các lớp tấn công thiểu số
    print("-> Đang tính toán sample_weight (cân bằng lớp)...")
    sample_weights_train = compute_sample_weight(class_weight='balanced', y=y_train)
    
    # 3. Khởi tạo mô hình XGBoost
    print("-> Khởi tạo XGBClassifier với tree_method='hist'...")
    model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        tree_method='hist',
        objective='multi:softprob',
        num_class=4,
        eval_metric='mlogloss',
        early_stopping_rounds=15,
        random_state=random_state,
        n_jobs=-1
    )
    
    # 4. Huấn luyện mô hình
    print("-> Đang huấn luyện mô hình...")
    start_train = time.time()
    model.fit(
        X_train, y_train,
        sample_weight=sample_weights_train,
        eval_set=[(X_val, y_val)],
        verbose=10
    )
    train_time = time.time() - start_train
    print(f"-> Huấn luyện xong trong {train_time:.1f} giây (tương đương {train_time/60:.2f} phút)!")
    
    # 5. Đánh giá trên tập Test
    print("-> Đang đánh giá trên tập kiểm tra độc lập (Test Set)...")
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    
    results = evaluate_predictions(
        y_true=y_test,
        y_pred=y_pred,
        y_prob=y_prob,
        model_name="XGBoost(hist, depth=6)",
        execution_time_sec=train_time
    )
    
    # Đo độ trễ
    print("-> Đang đo độ trễ suy luận...")
    latency = measure_inference_latency(model, X_test)
    
    # 6. In và lưu báo cáo
    md_content = format_markdown_report(results, latency)
    
    # Bổ sung Top Feature Importance
    try:
        importance = model.feature_importances_
        sorted_idx = np.argsort(importance)[::-1][:15]
        md_content += "\n## Top 15 Đặc trưng quan trọng nhất (Feature Importance - Gain)\n"
        md_content += "| Hạng | Tên đặc trưng | Điểm quan trọng |\n"
        md_content += "| :---: | :--- | ---: |\n"
        for rank, idx in enumerate(sorted_idx, 1):
            md_content += f"| {rank} | `{feature_cols[idx]}` | {importance[idx]:.4f} |\n"
    except Exception as e:
        print(f"Warning feature importance: {e}")
        
    print("\n" + md_content)
    
    # Lưu file báo cáo vào ngay trong folder ml_engine/xgboost/
    report_path = os.path.join(MODEL_DIR, "results.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\n[OK] Đã lưu báo cáo tại: {report_path}")
    
    # Đồng thời copy sang reports/ chung của dự án
    shared_report = os.path.join(PROJECT_ROOT, "reports", "07_xgboost_results.md")
    with open(shared_report, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    # 7. Đóng gói mô hình .joblib ngay trong folder ml_engine/xgboost/
    model_save_path = os.path.join(MODEL_DIR, "xgboost_model.joblib")
    joblib.dump({
        "model": model,
        "feature_cols": feature_cols,
        "class_names": CLASS_NAMES,
        "metrics": results
    }, model_save_path)
    print(f"[OK] Đã đóng gói mô hình tại: {model_save_path}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình XGBoost")
    parser.add_argument("--sample-ratio", type=float, default=None, help="Tỷ lệ mẫu (0.01 đến 1.0)")
    parser.add_argument("--n-estimators", type=int, default=100, help="Số cây")
    parser.add_argument("--max-depth", type=int, default=6, help="Độ sâu tối đa")
    parser.add_argument("--lr", type=float, default=0.1, help="Learning rate")
    args = parser.parse_args()
    
    train_xgboost(
        sample_ratio=args.sample_ratio,
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.lr
    )
