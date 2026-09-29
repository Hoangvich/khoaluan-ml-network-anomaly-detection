import os
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

LABEL_MAP = {
    'BENIGN': 0,
    'BruteForce': 1,
    'DoS/DDoS': 2,
    'PortScan': 3
}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}
CLASS_NAMES = ['BENIGN', 'BruteForce', 'DoS/DDoS', 'PortScan']
META_COLS = ['label', 'attack_subtype', 'source_dataset', 'source_file', 'group_id']

def load_data(parquet_path="data/processed/unified.parquet", sample_ratio=None, random_state=42):
    """
    Doc du lieu tu unified.parquet va tra ve X, y, groups, metadata.
    """
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Khong tim thay tap tin {parquet_path}")

    df = pd.read_parquet(parquet_path)
    
    if sample_ratio is not None and 0.0 < sample_ratio < 1.0:
        # Lay mau phan tang theo nhan de debug hoac chay thu nhanh tren CPU
        df = df.groupby('label', group_keys=False).sample(frac=sample_ratio, random_state=random_state).reset_index(drop=True)

    feature_cols = [c for c in df.columns if c not in META_COLS]
    X = df[feature_cols].copy()
    y = df['label'].map(LABEL_MAP).astype(np.int8)
    groups = df['group_id']
    
    return X, y, groups, feature_cols, df

def get_train_val_test_split(parquet_path="data/processed/unified.parquet", sample_ratio=None, random_state=42):
    """
    Chia train/val/test theo group_id (StratifiedGroupKFold) chong ro ri du lieu.
    Ty le: 70% Train, 15% Validation, 15% Test.
    """
    X, y, groups, feature_cols, df = load_data(parquet_path, sample_ratio, random_state)
    
    # Buoc 1: Tach 15% test truoc bang StratifiedGroupKFold (n_splits=7, 1 fold ~= 14.3%)
    sgkf_test = StratifiedGroupKFold(n_splits=7, shuffle=True, random_state=random_state)
    train_val_idx, test_idx = next(sgkf_test.split(X, y, groups))
    
    X_train_val = X.iloc[train_val_idx]
    y_train_val = y.iloc[train_val_idx]
    groups_train_val = groups.iloc[train_val_idx]
    
    X_test = X.iloc[test_idx].copy()
    y_test = y.iloc[test_idx].copy()
    
    # Buoc 2: Tach tiep trong phan con lai de lay 15% validation tren tong the (khoang 1/6 phan con lai)
    sgkf_val = StratifiedGroupKFold(n_splits=6, shuffle=True, random_state=random_state)
    train_idx_sub, val_idx_sub = next(sgkf_val.split(X_train_val, y_train_val, groups_train_val))
    
    X_train = X_train_val.iloc[train_idx_sub].copy()
    y_train = y_train_val.iloc[train_idx_sub].copy()
    
    X_val = X_train_val.iloc[val_idx_sub].copy()
    y_val = y_train_val.iloc[val_idx_sub].copy()
    
    # Kiem tra Assert PASS khong co group nao bi ro ri giua train/val/test
    train_groups = set(groups.iloc[train_val_idx[train_idx_sub]])
    val_groups = set(groups.iloc[train_val_idx[val_idx_sub]])
    test_groups = set(groups.iloc[test_idx])
    
    assert len(train_groups.intersection(test_groups)) == 0, "Ro ri group giua Train va Test!"
    assert len(train_groups.intersection(val_groups)) == 0, "Ro ri group giua Train va Val!"
    assert len(val_groups.intersection(test_groups)) == 0, "Ro ri group giua Val va Test!"
    
    return X_train, y_train, X_val, y_val, X_test, y_test, feature_cols
