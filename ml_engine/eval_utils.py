import time
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    accuracy_score,
    roc_auc_score,
    average_precision_score
)
from ml_engine.data_loader import CLASS_NAMES

def calculate_fpr_per_class(cm):
    """
    Tinh False Positive Rate (FPR) cho tung lop tu Confusion Matrix.
    FPR = FP / (FP + TN)
    """
    num_classes = cm.shape[0]
    fpr_list = []
    total_samples = np.sum(cm)
    for c in range(num_classes):
        tp = cm[c, c]
        fn = np.sum(cm[c, :]) - tp
        fp = np.sum(cm[:, c]) - tp
        tn = total_samples - (tp + fn + fp)
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        fpr_list.append(fpr)
    return fpr_list

def evaluate_predictions(y_true, y_pred, y_prob=None, model_name="Model", execution_time_sec=0.0):
    """
    Ham danh gia chuan hoa tra ve dict ket qua day du va chuoi Markdown de bao cao.
    """
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    weighted_f1 = f1_score(y_true, y_pred, average='weighted')
    
    clf_report = classification_report(
        y_true, y_pred, target_names=CLASS_NAMES, output_dict=True, digits=4
    )
    cm = confusion_matrix(y_true, y_pred)
    fpr_per_class = calculate_fpr_per_class(cm)
    
    # Tinh AUC neu co xac suat du doan
    auc_dict = {}
    pr_auc_dict = {}
    macro_auc = None
    if y_prob is not None:
        try:
            # One-vs-Rest ROC-AUC
            macro_auc = roc_auc_score(y_true, y_prob, multi_class='ovr', average='macro')
            for i, name in enumerate(CLASS_NAMES):
                y_true_bin = (y_true == i).astype(int)
                if len(np.unique(y_true_bin)) > 1:
                    auc_dict[name] = float(roc_auc_score(y_true_bin, y_prob[:, i]))
                    pr_auc_dict[name] = float(average_precision_score(y_true_bin, y_prob[:, i]))
                else:
                    auc_dict[name] = 1.0
                    pr_auc_dict[name] = 1.0
        except Exception as e:
            print(f"Warning AUC calculation: {e}")

    results = {
        "model_name": model_name,
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(weighted_f1),
        "macro_auc": float(macro_auc) if macro_auc is not None else None,
        "seconds": float(execution_time_sec),
        "classification_report": clf_report,
        "confusion_matrix": cm.tolist(),
        "fpr_per_class": {CLASS_NAMES[i]: float(fpr_per_class[i]) for i in range(len(CLASS_NAMES))},
        "auc_per_class": auc_dict,
        "pr_auc_per_class": pr_auc_dict
    }
    
    return results

def measure_inference_latency(model, X_sample, n_runs=10, is_pipeline=False):
    """
    Do do tre suy luan tren 1.000 luong va 1 luong don le.
    """
    if len(X_sample) < 1000:
        batch_1000 = X_sample
    else:
        batch_1000 = X_sample.iloc[:1000] if hasattr(X_sample, 'iloc') else X_sample[:1000]
        
    single_flow = X_sample.iloc[:1] if hasattr(X_sample, 'iloc') else X_sample[:1]
    
    # Warmup
    _ = model.predict(batch_1000)
    
    # Batch 1000 latency
    start = time.perf_counter()
    for _ in range(n_runs):
        _ = model.predict(batch_1000)
    batch_latency_ms = ((time.perf_counter() - start) / n_runs) * 1000
    
    # Single flow latency
    start = time.perf_counter()
    for _ in range(n_runs * 10):
        _ = model.predict(single_flow)
    single_latency_ms = ((time.perf_counter() - start) / (n_runs * 10)) * 1000
    
    return {
        "batch_1000_latency_ms": float(batch_latency_ms),
        "single_flow_latency_ms": float(single_latency_ms)
    }

def format_markdown_report(results, latency=None):
    """
    Tao bao cao Markdown dep mat tu ket qua danh gia.
    """
    md = []
    md.append(f"# Ket qua danh gia mo hinh: `{results['model_name']}`\n")
    md.append(f"- **Thoi gian huan luyen:** {results['seconds']:.1f}s")
    md.append(f"- **Accuracy:** {results['accuracy'] * 100:.2f}%")
    md.append(f"- **Macro F1:** {results['macro_f1']:.4f}")
    md.append(f"- **Weighted F1:** {results['weighted_f1']:.4f}")
    if results.get('macro_auc'):
        md.append(f"- **Macro ROC-AUC:** {results['macro_auc']:.4f}")
    if latency:
        md.append(f"- **Do tre tren 1.000 luong:** {latency['batch_1000_latency_ms']:.2f} ms")
        md.append(f"- **Do tre 1 luong don le:** {latency['single_flow_latency_ms']:.4f} ms")
        
    md.append("\n## Bang chi tiet tung lop (Classification Report & FPR)\n")
    md.append("| Lop | Precision | Recall | F1-Score | FPR | Support |")
    md.append("| :--- | :---: | :---: | :---: | :---: | ---: |")
    
    for c in CLASS_NAMES:
        row = results['classification_report'][c]
        fpr = results['fpr_per_class'].get(c, 0.0)
        md.append(f"| **{c}** | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1-score']:.4f} | {fpr:.4f} | {int(row['support']):,} |")
        
    md.append("\n## Ma tran nham lan (Confusion Matrix)\n")
    md.append("| That \\ Du doan | " + " | ".join(CLASS_NAMES) + " |")
    md.append("| :--- | " + " | ".join([":---:"] * len(CLASS_NAMES)) + " |")
    
    cm = np.array(results['confusion_matrix'])
    for i, c in enumerate(CLASS_NAMES):
        row_str = " | ".join([f"{int(x):,}" for x in cm[i]])
        md.append(f"| **{c}** | {row_str} |")
        
    return "\n".join(md)
