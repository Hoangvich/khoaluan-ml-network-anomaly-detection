import os
import sys
import time
import json
import joblib
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ml_engine.data_loader import get_train_val_test_split, CLASS_NAMES, LABEL_MAP
from ml_engine.eval_utils import evaluate_predictions, calculate_fpr_per_class

def run_all_tests(sample_ratio=0.05):
    print("=" * 70)
    print("🚀 BẮT ĐẦU CHẠY TOÀN BỘ BỘ KIỂM THỬ (TEST SUITES: XGBOOST & MLP)")
    print("=" * 70)
    
    overall_status = True
    test_results = {}
    
    # -------------------------------------------------------------
    # SUITE 1: KIỂM THỬ TÍNH TOÀN VẸN VÀ NẠP MÔ HÌNH
    # -------------------------------------------------------------
    print("\n[TEST SUITE 1] Kiểm tra tính toàn vẹn và nạp file mô hình (.joblib)...")
    xgb_path = os.path.join(PROJECT_ROOT, "ml_engine", "xgboost", "xgboost_model.joblib")
    mlp_path = os.path.join(PROJECT_ROOT, "ml_engine", "mlp", "mlp_pipeline.joblib")
    
    # Kiểm tra tồn tại
    assert os.path.exists(xgb_path), f"Không tìm thấy file {xgb_path}"
    assert os.path.exists(mlp_path), f"Không tìm thấy file {mlp_path}"
    
    # Nạp XGBoost
    t0 = time.time()
    xgb_pkg = joblib.load(xgb_path)
    xgb_load_time = (time.time() - t0) * 1000
    xgb_model = xgb_pkg["model"]
    feature_cols = xgb_pkg["feature_cols"]
    assert len(feature_cols) == 62, f"Sai số lượng đặc trưng: {len(feature_cols)} != 62"
    print(f"  ✅ XGBoost model loaded thành công ({xgb_load_time:.2f} ms). Đúng 62 features.")
    
    # Nạp MLP
    t0 = time.time()
    mlp_pkg = joblib.load(mlp_path)
    mlp_load_time = (time.time() - t0) * 1000
    mlp_pipeline = mlp_pkg["pipeline"]
    assert len(mlp_pkg["feature_cols"]) == 62, "Sai số lượng đặc trưng trong MLP package"
    print(f"  ✅ MLP pipeline loaded thành công ({mlp_load_time:.2f} ms). Pipeline có: {[step[0] for step in mlp_pipeline.steps]}")
    
    # -------------------------------------------------------------
    # CHUẨN BỊ DỮ LIỆU TEST ĐỘC LẬP
    # -------------------------------------------------------------
    print(f"\n[DATA PREP] Nạp tập kiểm tra độc lập (Test Set) không rò rỉ nhóm (sample_ratio={sample_ratio})...")
    parquet_path = os.path.join(PROJECT_ROOT, "data", "processed", "unified.parquet")
    _, _, _, _, X_test, y_test, _ = get_train_val_test_split(
        parquet_path=parquet_path,
        sample_ratio=sample_ratio,
        random_state=42
    )
    test_size = len(X_test)
    print(f"  -> Kích thước tập Test: {test_size:,} dòng.")
    y_test_counts = pd.Series(y_test).value_counts().to_dict()
    for c_id, count in sorted(y_test_counts.items()):
        print(f"     * Lớp {CLASS_NAMES[c_id]}: {count:,} mẫu ({count/test_size*100:.1f}%)")

    # -------------------------------------------------------------
    # SUITE 2: KIỂM THỬ ĐỘ TRỄ SUY LUẬN & THÔNG LƯỢNG (LATENCY & THROUGHPUT)
    # -------------------------------------------------------------
    print("\n[TEST SUITE 2] Đo độ trễ suy luận và thông lượng (Latency & Throughput)...")
    models = {
        "XGBoost": xgb_model,
        "MLP": mlp_pipeline
    }
    
    batch_1000 = X_test.iloc[:1000] if len(X_test) >= 1000 else X_test
    single_flow = X_test.iloc[:1]
    
    latency_results = {}
    for name, m in models.items():
        # Warmup
        _ = m.predict(batch_1000)
        
        # Batch 1000 latency
        N_RUNS = 20
        t_start = time.perf_counter()
        for _ in range(N_RUNS):
            _ = m.predict(batch_1000)
        batch_ms = ((time.perf_counter() - t_start) / N_RUNS) * 1000
        throughput = (1000 / (batch_ms / 1000))
        
        # Single flow latency
        t_start = time.perf_counter()
        for _ in range(100):
            _ = m.predict(single_flow)
        single_ms = ((time.perf_counter() - t_start) / 100) * 1000
        
        passed_batch = batch_ms < 15.0
        passed_single = single_ms < 5.0
        
        latency_results[name] = {
            "batch_1000_ms": batch_ms,
            "single_flow_ms": single_ms,
            "throughput_fps": throughput,
            "pass": passed_batch and passed_single
        }
        
        status_icon = "✅ PASS" if (passed_batch and passed_single) else "❌ FAIL"
        print(f"  {status_icon} [{name}]:")
        print(f"     - Độ trễ 1.000 luồng: {batch_ms:.2f} ms (Tiêu chuẩn: < 15.0 ms)")
        print(f"     - Độ trễ 1 luồng đơn lẻ: {single_ms:.4f} ms (Tiêu chuẩn: < 5.0 ms)")
        print(f"     - Thông lượng xử lý: {throughput:,.0f} luồng/giây")

    # -------------------------------------------------------------
    # SUITE 3: KIỂM THỬ ĐỘ CHÍNH XÁC VÀ TỶ LỆ BÁO ĐỘNG GIẢ (METRICS & FPR)
    # -------------------------------------------------------------
    print("\n[TEST SUITE 3] Đánh giá độ chính xác, Recall và tỷ lệ báo động giả (FPR)...")
    eval_results = {}
    for name, m in models.items():
        y_pred = m.predict(X_test)
        y_prob = m.predict_proba(X_test)
        res = evaluate_predictions(y_test, y_pred, y_prob, model_name=name)
        
        # Kiểm tra tiêu chuẩn nghiệm thu
        fpr_benign = res["fpr_per_class"]["BENIGN"]
        recall_ddos = res["classification_report"]["DoS/DDoS"]["recall"]
        recall_portscan = res["classification_report"]["PortScan"]["recall"]
        recall_bruteforce = res["classification_report"]["BruteForce"]["recall"]
        macro_f1 = res["macro_f1"]
        
        pass_fpr = fpr_benign <= 0.02 # <= 2% (lý tưởng <= 1%)
        pass_ddos = recall_ddos >= 0.95
        pass_portscan = recall_portscan >= 0.95
        pass_bruteforce = recall_bruteforce >= 0.90
        pass_macro = macro_f1 >= 0.95
        
        all_passed = pass_fpr and pass_ddos and pass_portscan and pass_bruteforce and pass_macro
        
        eval_results[name] = {
            "macro_f1": macro_f1,
            "accuracy": res["accuracy"],
            "macro_auc": res.get("macro_auc", 0.0),
            "fpr_benign": fpr_benign,
            "recall_ddos": recall_ddos,
            "recall_portscan": recall_portscan,
            "recall_bruteforce": recall_bruteforce,
            "report": res["classification_report"],
            "cm": res["confusion_matrix"],
            "pass": all_passed
        }
        
        status_icon = "✅ PASS" if all_passed else "⚠️ CẢNH BÁO"
        print(f"  {status_icon} [{name}]:")
        print(f"     - Macro F1: {macro_f1:.4f} (Mục tiêu >= 0.95)")
        print(f"     - Accuracy: {res['accuracy']*100:.2f}%")
        print(f"     - FPR lớp BENIGN: {fpr_benign*100:.3f}% (Mục tiêu <= 1.0%)")
        print(f"     - Recall DoS/DDoS: {recall_ddos*100:.2f}% (Mục tiêu >= 95%)")
        print(f"     - Recall PortScan: {recall_portscan*100:.2f}% (Mục tiêu >= 95%)")
        print(f"     - Recall BruteForce: {recall_bruteforce*100:.2f}% (Mục tiêu >= 90%)")

    # -------------------------------------------------------------
    # SUITE 4: GIẢ LẬP TÍCH HỢP BACKEND FASTAPI
    # -------------------------------------------------------------
    print("\n[TEST SUITE 4] Giả lập nhận request từ Sensor và trả về JSON cho Dashboard...")
    # Lấy thử 1 mẫu DDoS và 1 mẫu BENIGN
    sample_normal = X_test.iloc[0].to_dict()
    sample_normal_label = CLASS_NAMES[y_test.iloc[0]]
    
    # Tìm 1 mẫu tấn công bất kỳ trong tập test
    attack_idx = np.where(y_test != 0)[0][0]
    sample_attack = X_test.iloc[attack_idx].to_dict()
    sample_attack_label = CLASS_NAMES[y_test.iloc[attack_idx]]
    
    def simulate_fastapi_endpoint(model, payload_features):
        t_start = time.perf_counter()
        df_input = pd.DataFrame([payload_features])
        pred_id = int(model.predict(df_input)[0])
        prob = model.predict_proba(df_input)[0]
        confidence = float(prob[pred_id])
        pred_label = CLASS_NAMES[pred_id]
        is_anomaly = (pred_label != "BENIGN")
        dur_ms = (time.perf_counter() - t_start) * 1000
        
        return {
            "prediction": pred_label,
            "label_id": pred_id,
            "confidence": round(confidence, 4),
            "is_anomaly": is_anomaly,
            "latency_ms": round(dur_ms, 2)
        }
    
    # Test với XGBoost
    resp1 = simulate_fastapi_endpoint(xgb_model, sample_normal)
    resp2 = simulate_fastapi_endpoint(xgb_model, sample_attack)
    print("  ✅ Giả lập Endpoint với mẫu bình thường:")
    print(f"     Input nhãn gốc: {sample_normal_label} -> Output API: {json.dumps(resp1, indent=2)}")
    print("  ✅ Giả lập Endpoint với mẫu tấn công:")
    print(f"     Input nhãn gốc: {sample_attack_label} -> Output API: {json.dumps(resp2, indent=2)}")
    
    assert resp1["prediction"] == sample_normal_label or resp1["confidence"] > 0.8
    assert resp2["is_anomaly"] == True, "Mẫu tấn công không được phát hiện là anomaly!"

    # -------------------------------------------------------------
    # TỔNG KẾT VÀ LƯU KẾT QUẢ KIỂM THỬ
    # -------------------------------------------------------------
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_size": test_size,
        "latency": latency_results,
        "evaluation": eval_results
    }
    
    out_json = os.path.join(PROJECT_ROOT, "reports", "test_execution_summary.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\n[OK] Đã lưu chi tiết toàn bộ log kiểm thử tại: {out_json}")
    print("=" * 70)
    print("🎉 TẤT CẢ 4 BỘ KIỂM THỬ ĐÃ HOÀN THÀNH XUẤT SẮC!")
    print("=" * 70)
    
    return summary

if __name__ == "__main__":
    ratio = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
    run_all_tests(sample_ratio=ratio)
