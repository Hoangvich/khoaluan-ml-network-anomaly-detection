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

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

from ml_engine.data_loader import get_train_val_test_split, CLASS_NAMES
from ml_engine.eval_utils import evaluate_predictions, measure_inference_latency, format_markdown_report

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

def train_mlp(sample_ratio=None, hidden_layers=(128, 64), max_iter=30, batch_size=1024, lr=0.001, random_state=42):
    print("=" * 60)
    print(f"BẮT ĐẦU HUẤN LUYỆN MLP (Multi-Layer Perceptron)")
    print(f"Kiến trúc: Input(62) -> {hidden_layers} -> Output(4)")
    print(f"Tỷ lệ mẫu: {sample_ratio if sample_ratio else '100% full dataset'}")
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
    
    # 2. Xây dựng Pipeline: StandardScaler + MLPClassifier
    print("-> Khởi tạo Pipeline chuẩn hóa StandardScaler + MLPClassifier...")
    scaler = StandardScaler()
    mlp = MLPClassifier(
        hidden_layer_sizes=hidden_layers,
        activation='relu',
        solver='adam',
        alpha=1e-4,
        batch_size=batch_size,
        learning_rate_init=lr,
        learning_rate='adaptive',
        max_iter=max_iter,
        early_stopping=True,
        n_iter_no_change=10,
        random_state=random_state,
        verbose=True
    )
    
    pipeline = Pipeline([
        ('scaler', scaler),
        ('mlp', mlp)
    ])
    
    # 3. Huấn luyện mô hình
    print("-> Đang huấn luyện mô hình MLP (chuẩn hóa chỉ fit trên tập Train)...")
    start_train = time.time()
    pipeline.fit(X_train, y_train)
    train_time = time.time() - start_train
    print(f"-> Huấn luyện xong trong {train_time:.1f} giây (tương đương {train_time/60:.2f} phút)!")
    
    # 4. Đánh giá trên tập Test
    print("-> Đang đánh giá trên tập kiểm tra độc lập (Test Set)...")
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)
    
    results = evaluate_predictions(
        y_true=y_test,
        y_pred=y_pred,
        y_prob=y_prob,
        model_name=f"MLP{hidden_layers}",
        execution_time_sec=train_time
    )
    
    # Đo độ trễ
    print("-> Đang đo độ trễ suy luận...")
    latency = measure_inference_latency(pipeline, X_test)
    
    # 5. In và lưu báo cáo
    md_content = format_markdown_report(results, latency)
    md_content += f"\n## Thông số kiến trúc mô hình\n"
    md_content += f"- **Các lớp ẩn (Hidden Layers):** `{hidden_layers}`\n"
    md_content += f"- **Hàm kích hoạt:** `ReLU`\n"
    md_content += f"- **Thuật toán tối ưu:** `Adam` (lr={lr}, batch_size={batch_size})\n"
    md_content += f"- **Số epoch thực tế:** {mlp.n_iter_}\n"
    md_content += f"- **Loss cuối cùng:** {mlp.loss_:.6f}\n"
    
    print("\n" + md_content)
    
    # Lưu file báo cáo vào ngay trong folder ml_engine/mlp/
    report_path = os.path.join(MODEL_DIR, "results.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\n[OK] Đã lưu báo cáo tại: {report_path}")
    
    # Đồng thời copy sang reports/ chung của dự án
    shared_report = os.path.join(PROJECT_ROOT, "reports", "08_mlp_results.md")
    with open(shared_report, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    # 6. Đóng gói pipeline duy nhất (.joblib) ngay trong folder ml_engine/mlp/
    model_save_path = os.path.join(MODEL_DIR, "mlp_pipeline.joblib")
    joblib.dump({
        "pipeline": pipeline,
        "feature_cols": feature_cols,
        "class_names": CLASS_NAMES,
        "metrics": results
    }, model_save_path)
    print(f"[OK] Đã đóng gói pipeline tại: {model_save_path}")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình MLP")
    parser.add_argument("--sample-ratio", type=float, default=None, help="Tỷ lệ mẫu (0.01 đến 1.0)")
    parser.add_argument("--max-iter", type=int, default=30, help="Số epoch tối đa")
    parser.add_argument("--batch-size", type=int, default=1024, help="Kích thước mini-batch")
    parser.add_argument("--lr", type=float, default=0.001, help="Tốc độ học")
    args = parser.parse_args()
    
    train_mlp(
        sample_ratio=args.sample_ratio,
        max_iter=args.max_iter,
        batch_size=args.batch_size,
        lr=args.lr
    )
