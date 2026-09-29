# Ket qua danh gia mo hinh: `MLP(128, 64)`

- **Thoi gian huan luyen:** 3.6s
- **Accuracy:** 99.45%
- **Macro F1:** 0.9896
- **Weighted F1:** 0.9945
- **Macro ROC-AUC:** 0.9995
- **Do tre tren 1.000 luong:** 1.74 ms
- **Do tre 1 luong don le:** 0.9419 ms

## Bang chi tiet tung lop (Classification Report & FPR)

| Lop | Precision | Recall | F1-Score | FPR | Support |
| :--- | :---: | :---: | :---: | :---: | ---: |
| **BENIGN** | 0.9961 | 0.9969 | 0.9965 | 0.0120 | 7,110 |
| **BruteForce** | 0.9932 | 0.9667 | 0.9797 | 0.0002 | 300 |
| **DoS/DDoS** | 0.9892 | 0.9880 | 0.9886 | 0.0022 | 1,582 |
| **PortScan** | 0.9890 | 0.9978 | 0.9934 | 0.0006 | 452 |

## Ma tran nham lan (Confusion Matrix)

| That \ Du doan | BENIGN | BruteForce | DoS/DDoS | PortScan |
| :--- | :---: | :---: | :---: | :---: |
| **BENIGN** | 7,088 | 0 | 17 | 5 |
| **BruteForce** | 10 | 290 | 0 | 0 |
| **DoS/DDoS** | 17 | 2 | 1,563 | 0 |
| **PortScan** | 1 | 0 | 0 | 451 |
## Thông số kiến trúc mô hình
- **Các lớp ẩn (Hidden Layers):** `(128, 64)`
- **Hàm kích hoạt:** `ReLU`
- **Thuật toán tối ưu:** `Adam` (lr=0.001, batch_size=512)
- **Số epoch thực tế:** 20
- **Loss cuối cùng:** 0.020697
