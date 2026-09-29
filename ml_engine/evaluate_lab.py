import os
import sys
import joblib
import pandas as pd
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml_engine.eval_utils import evaluate_predictions, CLASS_NAMES

def evaluate_on_lab():
    lab_path = os.path.join(PROJECT_ROOT, "data", "processed", "lab_traffic_cleaned.parquet")
    if not os.path.exists(lab_path):
        print(f"Chưa có file {lab_path}")
        return
        
    df_lab = pd.read_parquet(lab_path)
    meta = ['label', 'attack_subtype', 'source_dataset', 'source_file', 'group_id']
    X_lab = df_lab.drop(columns=meta)
    label_map = {'BENIGN': 0, 'BruteForce': 1, 'DoS/DDoS': 2, 'PortScan': 3}
    y_lab = df_lab['label'].map(label_map).astype(np.int8)
    
    print("=" * 70)
    print("🎯 KẾT QUẢ KIỂM THỬ THỰC TẾ TRÊN LƯU LƯỢNG MẠNG PHÒNG LAB (133,056 LUỒNG)")
    print("=" * 70)
    
    # 1. XGBoost
    xgb_path = os.path.join(PROJECT_ROOT, "ml_engine", "xgboost", "xgboost_model.joblib")
    xgb_pkg = joblib.load(xgb_path)
    model_xgb = xgb_pkg['model']
    y_pred_xgb = model_xgb.predict(X_lab)
    y_prob_xgb = model_xgb.predict_proba(X_lab)
    res_xgb = evaluate_predictions(y_lab, y_pred_xgb, y_prob_xgb, model_name="XGBoost on Lab Traffic")
    
    print(f"\n📊 [XGBOOST TRÊN MẠNG LAB THỰC TẾ]")
    print(f"- Accuracy tổng thể: {res_xgb['accuracy']*100:.2f}%")
    print(f"- Macro F1-Score: {res_xgb['macro_f1']:.4f}")
    print("\nChi tiết từng lớp:")
    for c in CLASS_NAMES:
        row = res_xgb['classification_report'][c]
        print(f"  * {c:12s}: Recall = {row['recall']*100:.2f}% | Precision = {row['precision']*100:.2f}% | Support = {int(row['support']):,}")
        
    # 2. MLP
    mlp_path = os.path.join(PROJECT_ROOT, "ml_engine", "mlp", "mlp_pipeline.joblib")
    mlp_pkg = joblib.load(mlp_path)
    pipe_mlp = mlp_pkg['pipeline']
    y_pred_mlp = pipe_mlp.predict(X_lab)
    y_prob_mlp = pipe_mlp.predict_proba(X_lab)
    res_mlp = evaluate_predictions(y_lab, y_pred_mlp, y_prob_mlp, model_name="MLP on Lab Traffic")
    
    print(f"\n📊 [MLP PIPELINE TRÊN MẠNG LAB THỰC TẾ]")
    print(f"- Accuracy tổng thể: {res_mlp['accuracy']*100:.2f}%")
    print(f"- Macro F1-Score: {res_mlp['macro_f1']:.4f}")
    print("\nChi tiết từng lớp:")
    for c in CLASS_NAMES:
        row = res_mlp['classification_report'][c]
        print(f"  * {c:12s}: Recall = {row['recall']*100:.2f}% | Precision = {row['precision']*100:.2f}% | Support = {int(row['support']):,}")
        
    print("\n" + "=" * 70)

if __name__ == "__main__":
    evaluate_on_lab()
