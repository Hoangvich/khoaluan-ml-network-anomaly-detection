# Ket qua danh gia mo hinh: `XGBoost(hist, depth=6)`

- **Thoi gian huan luyen:** 1.0s
- **Accuracy:** 98.73%
- **Macro F1:** 0.9846
- **Weighted F1:** 0.9874
- **Macro ROC-AUC:** 0.9998
- **Do tre tren 1.000 luong:** 3.38 ms
- **Do tre 1 luong don le:** 2.4922 ms

## Bang chi tiet tung lop (Classification Report & FPR)

| Lop | Precision | Recall | F1-Score | FPR | Support |
| :--- | :---: | :---: | :---: | :---: | ---: |
| **BENIGN** | 1.0000 | 0.9833 | 0.9916 | 0.0000 | 7,110 |
| **BruteForce** | 0.9740 | 1.0000 | 0.9868 | 0.0009 | 300 |
| **DoS/DDoS** | 0.9372 | 1.0000 | 0.9676 | 0.0135 | 1,582 |
| **PortScan** | 0.9869 | 0.9978 | 0.9923 | 0.0007 | 452 |

## Ma tran nham lan (Confusion Matrix)

| That \ Du doan | BENIGN | BruteForce | DoS/DDoS | PortScan |
| :--- | :---: | :---: | :---: | :---: |
| **BENIGN** | 6,991 | 7 | 106 | 6 |
| **BruteForce** | 0 | 300 | 0 | 0 |
| **DoS/DDoS** | 0 | 0 | 1,582 | 0 |
| **PortScan** | 0 | 1 | 0 | 451 |
## Top 15 Đặc trưng quan trọng nhất (Feature Importance - Gain)
| Hạng | Tên đặc trưng | Điểm quan trọng |
| :---: | :--- | ---: |
| 1 | `Total Length of Fwd Packets` | 0.1857 |
| 2 | `Bwd Header Length` | 0.1820 |
| 3 | `Average Packet Size` | 0.1593 |
| 4 | `Bwd Packet Length Min` | 0.1461 |
| 5 | `Bwd Packet Length Mean` | 0.0429 |
| 6 | `Fwd IAT Min` | 0.0296 |
| 7 | `Init_Win_bytes_backward` | 0.0227 |
| 8 | `Total Backward Packets` | 0.0227 |
| 9 | `Flow IAT Std` | 0.0214 |
| 10 | `Total Fwd Packets` | 0.0213 |
| 11 | `Active Max` | 0.0209 |
| 12 | `Packet Length Std` | 0.0166 |
| 13 | `Fwd IAT Total` | 0.0161 |
| 14 | `min_seg_size_forward` | 0.0129 |
| 15 | `Fwd PSH Flags` | 0.0091 |
