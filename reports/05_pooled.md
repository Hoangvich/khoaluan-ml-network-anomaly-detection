# Buoc 5 - Giao thuc A: pooled (group-aware split)

- Split 70/15/15 theo `group_id` (StratifiedGroupKFold, seed=42)
- train **2,260,546** / val **452,110** / test **452,110**
- Assert PASS: khong mot `group_id` nao xuat hien o hai tap khac nhau

## Phan bo lop

| Lop | train | val | test |
|---|---:|---:|---:|
| BENIGN | 1,779,265 | 355,854 | 355,854 |
| DDoS | 293,339 | 58,668 | 58,668 |
| PortScan | 113,037 | 22,608 | 22,608 |
| BruteForce | 74,905 | 14,980 | 14,980 |

## Ket qua (Bang A)

| Model | Dong train | Thoi gian | macro-F1 (val) | macro-F1 (test) |
|---|---:|---:|---:|---:|
| RandomForest(100) | 2,260,546 | 169s | 0.9983 | **0.9991** |
| DecisionTree(d=8) | 2,260,546 | 143s | 0.9943 | **0.9958** |
| HistGradientBoosting | 2,260,546 | 72s | 0.9934 | **0.9989** |
| LogisticRegression | 400,000 | 28s | 0.9141 | **0.9246** |

**Model tot nhat theo validation: `RandomForest(100)`**


### DecisionTree(d=8)

```
              precision    recall  f1-score   support

      BENIGN     0.9997    0.9982    0.9990    355854
  BruteForce     0.9985    0.9983    0.9984     14980
        DDoS     0.9988    0.9987    0.9987     58668
    PortScan     0.9749    0.9996    0.9871     22608

    accuracy                         0.9983    452110
   macro avg     0.9930    0.9987    0.9958    452110
weighted avg     0.9983    0.9983    0.9983    452110
```

Average Precision (PR-AUC) tung lop: `BENIGN`=0.9998, `BruteForce`=0.9972, `DDoS`=0.9988, `PortScan`=0.9943

Confusion matrix (hang = that, cot = du doan):

| that \ du doan | BENIGN | BruteForce | DDoS | PortScan |
|---|---|---|---|---|
| **BENIGN** | 355,202 | 22 | 70 | 560 |
| **BruteForce** | 24 | 14,955 | 1 | 0 |
| **DDoS** | 57 | 0 | 58,590 | 21 |
| **PortScan** | 10 | 0 | 0 | 22,598 |

### RandomForest(100)

```
              precision    recall  f1-score   support

      BENIGN     0.9999    0.9996    0.9997    355854
  BruteForce     1.0000    0.9995    0.9997     14980
        DDoS     0.9998    0.9993    0.9995     58668
    PortScan     0.9947    1.0000    0.9974     22608

    accuracy                         0.9996    452110
   macro avg     0.9986    0.9996    0.9991    452110
weighted avg     0.9996    0.9996    0.9996    452110
```

Average Precision (PR-AUC) tung lop: `BENIGN`=1.0000, `BruteForce`=0.9999, `DDoS`=1.0000, `PortScan`=0.9989

Confusion matrix (hang = that, cot = du doan):

| that \ du doan | BENIGN | BruteForce | DDoS | PortScan |
|---|---|---|---|---|
| **BENIGN** | 355,720 | 0 | 14 | 120 |
| **BruteForce** | 8 | 14,972 | 0 | 0 |
| **DDoS** | 41 | 0 | 58,627 | 0 |
| **PortScan** | 0 | 0 | 0 | 22,608 |

### HistGradientBoosting

```
              precision    recall  f1-score   support

      BENIGN     0.9999    0.9993    0.9996    355854
  BruteForce     0.9999    0.9999    0.9999     14980
        DDoS     0.9977    0.9994    0.9986     58668
    PortScan     0.9948    1.0000    0.9974     22608

    accuracy                         0.9994    452110
   macro avg     0.9981    0.9996    0.9989    452110
weighted avg     0.9994    0.9994    0.9994    452110
```

Average Precision (PR-AUC) tung lop: `BENIGN`=0.9999, `BruteForce`=0.9999, `DDoS`=0.9976, `PortScan`=0.9989

Confusion matrix (hang = that, cot = du doan):

| that \ du doan | BENIGN | BruteForce | DDoS | PortScan |
|---|---|---|---|---|
| **BENIGN** | 355,601 | 1 | 133 | 119 |
| **BruteForce** | 2 | 14,978 | 0 | 0 |
| **DDoS** | 33 | 0 | 58,635 | 0 |
| **PortScan** | 0 | 0 | 0 | 22,608 |

### LogisticRegression

```
              precision    recall  f1-score   support

      BENIGN     0.9984    0.9527    0.9750    355854
  BruteForce     0.8116    0.9991    0.8956     14980
        DDoS     0.8758    0.9914    0.9300     58668
    PortScan     0.8149    0.9991    0.8976     22608

    accuracy                         0.9616    452110
   macro avg     0.8752    0.9856    0.9246    452110
weighted avg     0.9672    0.9616    0.9627    452110
```

Average Precision (PR-AUC) tung lop: `BENIGN`=0.9991, `BruteForce`=0.9685, `DDoS`=0.9929, `PortScan`=0.9748

Confusion matrix (hang = that, cot = du doan):

| that \ du doan | BENIGN | BruteForce | DDoS | PortScan |
|---|---|---|---|---|
| **BENIGN** | 339,012 | 3,475 | 8,235 | 5,132 |
| **BruteForce** | 13 | 14,967 | 0 | 0 |
| **DDoS** | 505 | 0 | 58,163 | 0 |
| **PortScan** | 9 | 0 | 12 | 22,587 |

## Permutation importance - top 20 (RandomForest(100), 50,000 dong validation)

| # | Feature | Do giam macro-F1 | std |
|---:|---|---:|---:|
| 1 | `Init_Win_bytes_forward` | 0.00770 | 0.00013 |
| 2 | `Average Packet Size` | 0.00480 | 0.00005 |
| 3 | `Total Length of Fwd Packets` | 0.00464 | 0.00005 |
| 4 | `Fwd Packet Length Max` | 0.00417 | 0.00003 |
| 5 | `Packet Length Variance` | 0.00390 | 0.00001 |
| 6 | `Flow Packets/s` | 0.00385 | 0.00011 |
| 7 | `ACK Flag Count` | 0.00382 | 0.00008 |
| 8 | `Total Backward Packets` | 0.00379 | 0.00011 |
| 9 | `Max Packet Length` | 0.00378 | 0.00005 |
| 10 | `Packet Length Std` | 0.00370 | 0.00003 |
| 11 | `Fwd Header Length` | 0.00365 | 0.00012 |
| 12 | `Bwd Header Length` | 0.00362 | 0.00018 |
| 13 | `Bwd Packet Length Max` | 0.00309 | 0.00003 |
| 14 | `Flow IAT Std` | 0.00297 | 0.00022 |
| 15 | `act_data_pkt_fwd` | 0.00290 | 0.00012 |
| 16 | `Bwd Packet Length Min` | 0.00242 | 0.00002 |
| 17 | `Init_Win_bytes_backward` | 0.00198 | 0.00007 |
| 18 | `Min Packet Length` | 0.00192 | 0.00004 |
| 19 | `Fwd Packet Length Min` | 0.00186 | 0.00007 |
| 20 | `Total Fwd Packets` | 0.00183 | 0.00014 |

> Top-5: `Init_Win_bytes_forward`, `Average Packet Size`, `Total Length of Fwd Packets`, `Fwd Packet Length Max`, `Packet Length Variance`

> ⚠️ `Init_Win_bytes_forward` nam trong top-5. Day la fingerprint host (29200 cho moi attack 2017, 26883 cho 2018) -> ket qua Bang A can duoc doi chieu ky voi Bang B truoc khi tin.