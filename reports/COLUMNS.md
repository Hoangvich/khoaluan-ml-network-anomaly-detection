# Từ điển dữ liệu — 67 cột của `ALL.csv`

Bộ dữ liệu hợp nhất từ CIC-IDS2017, CSE-CIC-IDS2018 (ngày 14-02) và CIC-DDoS2019, phục vụ bài toán phân loại bốn lớp: `BENIGN`, `DoS/DDoS`, `PortScan`, `BruteForce`.

**3.305.401 dòng × 67 cột** = 62 đặc trưng đầu vào + 5 cột nhãn/siêu dữ liệu.

Mọi con số thống kê trong tài liệu này đều được tính trực tiếp từ dữ liệu, không phải ước lượng.

> \* Riêng dòng *Hạng permutation importance* được lấy từ một lần huấn luyện tham khảo chạy **trước** khi lọc các giá trị hỏng do tràn số. Hãy xem nó là chỉ dấu định tính về mức độ quan trọng tương đối của từng cột, không phải kết quả cuối cùng.

## Cách dùng nhanh

```python
import pandas as pd

df = pd.read_csv('ALL.csv')                       # hoặc:
df = pd.read_parquet('data/unified.parquet')      # nhanh hơn nhiều, giữ nguyên kiểu dữ liệu

META = ['label', 'attack_subtype', 'source_dataset', 'source_file', 'group_id']
X = df.drop(columns=META)     # 62 đặc trưng
y = df['label']
groups = df['group_id']       # BẮT BUỘC dùng cho StratifiedGroupKFold
```

> ⚠️ **Bốn cột `attack_subtype`, `source_dataset`, `source_file` và `group_id` tuyệt đối không được dùng làm đặc trưng.** Chúng mang thông tin về *nguồn gốc và cách gán nhãn* chứ không phải *hành vi mạng*; đưa vào mô hình sẽ cho kết quả hoàn hảo một cách giả tạo.

## Mục lục theo nhóm

| Nhóm | Số cột | Các cột |
|---|---:|---|
| [Cờ TCP](#cờ-tcp) | 9 | `ACK Flag Count`, `ECE Flag Count`, `FIN Flag Count`, `Fwd PSH Flags`, `Fwd URG Flags`, `PSH Flag Count`, `RST Flag Count`, `SYN Flag Count`, `URG Flag Count` |
| [Chu kỳ hoạt động và nghỉ](#chu-kỳ-hoạt-động-và-nghỉ) | 8 | `Active Max`, `Active Mean`, `Active Min`, `Active Std`, `Idle Max`, `Idle Mean`, `Idle Min`, `Idle Std` |
| [Kích thước gói (toàn luồng)](#kích-thước-gói-toàn-luồng) | 6 | `Average Packet Size`, `Max Packet Length`, `Min Packet Length`, `Packet Length Mean`, `Packet Length Std`, `Packet Length Variance` |
| [Header & cửa sổ TCP](#header--cửa-sổ-tcp) | 5 | `Bwd Header Length`, `Fwd Header Length`, `Init_Win_bytes_backward`, `Init_Win_bytes_forward`, `min_seg_size_forward` |
| [Khoảng cách giữa các gói (IAT)](#khoảng-cách-giữa-các-gói-iat) | 14 | `Bwd IAT Max`, `Bwd IAT Mean`, `Bwd IAT Min`, `Bwd IAT Std`, `Bwd IAT Total`, `Flow IAT Max`, `Flow IAT Mean`, `Flow IAT Min`, `Flow IAT Std`, `Fwd IAT Max`, `Fwd IAT Mean`, `Fwd IAT Min`, `Fwd IAT Std`, `Fwd IAT Total` |
| [Kích thước gói (theo hướng)](#kích-thước-gói-theo-hướng) | 8 | `Bwd Packet Length Max`, `Bwd Packet Length Mean`, `Bwd Packet Length Min`, `Bwd Packet Length Std`, `Fwd Packet Length Max`, `Fwd Packet Length Mean`, `Fwd Packet Length Min`, `Fwd Packet Length Std` |
| [Tốc độ](#tốc-độ) | 4 | `Bwd Packets/s`, `Flow Bytes/s`, `Flow Packets/s`, `Fwd Packets/s` |
| [Khác](#khác) | 2 | `Down/Up Ratio`, `act_data_pkt_fwd` |
| [Thời lượng](#thời-lượng) | 1 | `Flow Duration` |
| [Đếm gói & byte](#đếm-gói--byte) | 4 | `Total Backward Packets`, `Total Fwd Packets`, `Total Length of Bwd Packets`, `Total Length of Fwd Packets` |
| [Đặc trưng suy ra](#đặc-trưng-suy-ra) | 1 | `dst_port_class` |
| [Nhãn và siêu dữ liệu](#nhãn-và-siêu-dữ-liệu) | 5 | `label`, `attack_subtype`, `source_dataset`, `source_file`, `group_id` |

---

## Cờ TCP

### 1. `ACK Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 80,6% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,602 |
| Hạng permutation importance * | **7/20** |

**Là gì:** Số gói mang cờ ACK.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 19. `ECE Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 98,7% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,508 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ ECE, thông báo tắc nghẽn theo cơ chế ECN.

**Để làm gì:** Rất hiếm.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 20. `FIN Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 97,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,547 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ FIN, tức là đóng kết nối một cách lịch sự.

**Để làm gì:** Luồng tấn công thường bị ngắt đột ngột nên không có FIN.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 34. `Fwd PSH Flags`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 95,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,526 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số cờ PSH tính riêng cho hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 40. `Fwd URG Flags`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 100,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,500 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số cờ URG tính riêng cho hướng thuận.

**Để làm gì:** Trùng 99,996% với `CWE Flag Count` — cột đó đã bị loại bỏ.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 49. `PSH Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 65,4% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,843 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ PSH, yêu cầu đẩy dữ liệu lên ứng dụng ngay lập tức.

**Để làm gì:** Cao trong phiên tương tác như SSH hay HTTP, nên hữu ích cho brute force.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 1 | 1 |

### 53. `RST Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 98,7% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,508 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ RST, tức là từ chối hoặc đặt lại kết nối.

**Để làm gì:** Tín hiệu mạnh của quét cổng: cổng đóng sẽ trả về RST.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 54. `SYN Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 95,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,526 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ SYN, tức là mở kết nối.

**Để làm gì:** **Cảnh báo:** CICFlowMeter chỉ đếm một SYN cho mỗi luồng nên cột này gần như nhị phân, yếu hơn kỳ vọng đối với PortScan.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 59. `URG Flag Count`

| | |
|---|---|
| Đơn vị | số đếm |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 1 |
| Số giá trị phân biệt | 2 |
| Tỉ lệ bằng 0 | 96,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,524 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Số gói mang cờ URG, đánh dấu dữ liệu khẩn.

**Để làm gì:** Hiếm gặp trong lưu lượng thật.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

## Chu kỳ hoạt động và nghỉ

### 2. `Active Max`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 110.240.120 |
| Số giá trị phân biệt | 345.725 |
| Tỉ lệ bằng 0 | 81,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,598 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Phiên hoạt động liên tục dài nhất.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 3. `Active Mean`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 110.240.120 |
| Số giá trị phân biệt | 382.085 |
| Tỉ lệ bằng 0 | 81,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,598 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Thời gian trung bình luồng ở trạng thái hoạt động trước khi chuyển sang nghỉ.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 4. `Active Min`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 110.240.120 |
| Số giá trị phân biệt | 192.083 |
| Tỉ lệ bằng 0 | 81,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,598 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Phiên hoạt động liên tục ngắn nhất.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 5. `Active Std`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 74.200.000 |
| Số giá trị phân biệt | 253.608 |
| Tỉ lệ bằng 0 | 92,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `BENIGN` — 0,549 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn của thời gian hoạt động.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 41. `Idle Max`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 120.000.000 |
| Số giá trị phân biệt | 193.106 |
| Tỉ lệ bằng 0 | 80,9% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,628 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Khoảng nghỉ dài nhất.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 42. `Idle Mean`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 120.000.000 |
| Số giá trị phân biệt | 248.066 |
| Tỉ lệ bằng 0 | 80,9% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,627 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Thời gian nghỉ trung bình giữa các đợt hoạt động.

**Để làm gì:** Brute force tốc độ chậm có chu kỳ nghỉ đều đặn rất đặc trưng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 43. `Idle Min`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 120.000.000 |
| Số giá trị phân biệt | 274.854 |
| Tỉ lệ bằng 0 | 80,9% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,626 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Khoảng nghỉ ngắn nhất.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

### 44. `Idle Std`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 76.900.000 |
| Số giá trị phân biệt | 250.268 |
| Tỉ lệ bằng 0 | 91,5% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,544 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn của thời gian nghỉ.

**Để làm gì:** Gần bằng 0 nghĩa là nhịp nghỉ cố định — dấu hiệu công cụ tự động.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 0 |

## Kích thước gói (toàn luồng)

### 6. `Average Packet Size`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.20 / 93.50 / 3 893.33 |
| Số giá trị phân biệt | 210.718 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,974 |
| Hạng permutation importance * | **2/20** |

**Là gì:** Tổng byte chia tổng gói. Có liên hệ chính xác với `Packet Length Mean`: `Average Packet Size / Packet Length Mean = (n+1)/n`, với n là tổng số gói.

**Để làm gì:** Chính đẳng thức này được dùng làm **bằng chứng bảng map cột đúng ngữ nghĩa** — nó đạt 100% ở cả ba bộ dữ liệu.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 86 | 798.33 | 3 | 104.39 |

### 47. `Max Packet Length`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 1 / 134 / 64.440 |
| Số giá trị phân biệt | 5.691 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,928 |
| Hạng permutation importance * | **9/20** |

**Là gì:** Gói lớn nhất tính trên cả hai hướng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 114 | 1.472 | 6 | 976 |

### 48. `Min Packet Length`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 6 / 1.472 |
| Số giá trị phân biệt | 1.082 |
| Tỉ lệ bằng 0 | 41,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,803 |
| Hạng permutation importance * | **18/20** |

**Là gì:** Gói nhỏ nhất tính trên cả hai hướng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 6 | 6 | 0 | 0 |

### 50. `Packet Length Mean`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.17 / 72.20 / 3 337.14 |
| Số giá trị phân biệt | 213.129 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,983 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Kích thước gói trung bình trên toàn luồng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 66.20 | 744.69 | 2 | 102.07 |

### 51. `Packet Length Std`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 35.05 / 8 810.77 |
| Số giá trị phân biệt | 435.246 |
| Tỉ lệ bằng 0 | 17,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,790 |
| Hạng permutation importance * | **10/20** |

**Là gì:** Độ lệch chuẩn kích thước gói toàn luồng.

**Để làm gì:** Lưu lượng đồng nhất (độ lệch ≈ 0) rất đặc trưng cho flood và quét cổng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 37.53 | 2.68 | 3.46 | 203.74 |

### 52. `Packet Length Variance`

| | |
|---|---|
| Đơn vị | byte² |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 1 228.80 / 77.629.640 |
| Số giá trị phân biệt | 435.085 |
| Tỉ lệ bằng 0 | 17,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,790 |
| Hạng permutation importance * | **5/20** |

**Là gì:** Phương sai kích thước gói, bằng bình phương của `Packet Length Std`.

**Để làm gì:** Dư thừa về mặt toán học so với cột độ lệch chuẩn, nhưng vẫn giữ lại vì thang đo khác nhau giúp cây quyết định cắt ngưỡng dễ hơn.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 1 408.33 | 7.20 | 12 | 41 510.38 |

## Header & cửa sổ TCP

### 7. `Bwd Header Length`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 40 / 3.147.772 |
| Số giá trị phân biệt | 3.955 |
| Tỉ lệ bằng 0 | 17,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,941 |
| Hạng permutation importance * | **12/20** |

**Là gì:** Tổng độ dài phần header của các gói hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 40 | 0 | 20 | 712 |

### 28. `Fwd Header Length`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 64 / 134.480.896 |
| Số giá trị phân biệt | 4.277 |
| Tỉ lệ bằng 0 | 1,4% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,949 |
| Hạng permutation importance * | **11/20** |

**Là gì:** Tổng độ dài phần header của các gói hướng thuận.

**Để làm gì:** Suy ra được số gói và việc có dùng tùy chọn TCP hay không. Bộ 2017 chứa cột này hai lần; bản trùng đã bị loại. Dữ liệu gốc còn có 36.333 dòng mang giá trị âm do tràn số — đã loại bỏ ở bước 3.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 64 | 80 | 40 | 712 |

### 45. `Init_Win_bytes_backward`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | -1 / -1 / 65.535 |
| Số giá trị phân biệt | 13.306 |
| Tỉ lệ bằng 0 | 9,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,760 |
| Hạng permutation importance * | **17/20** |

**Là gì:** Kích thước cửa sổ TCP quảng bá trong gói SYN-ACK hướng ngược, `-1` nếu không có.

**Để làm gì:** Cũng mang rủi ro vân tay hệ điều hành như cột trên, nhưng ở mức độ nhẹ hơn.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| -1 | -1 | 0 | 230 |

### 46. `Init_Win_bytes_forward`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | -1 / 229 / 65.535 |
| Số giá trị phân biệt | 10.326 |
| Tỉ lệ bằng 0 | 2,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,865 |
| Hạng permutation importance * | **1/20** |

**Là gì:** Kích thước cửa sổ TCP quảng bá trong gói SYN hướng thuận. Giá trị `-1` nghĩa là không phải TCP, ví dụ luồng UDP.

**Để làm gì:** ⚠️ **Đây là cột rủi ro rò rỉ cao nhất trong toàn bộ dataset.** Nó là đặc trưng quan trọng nhất của mô hình (hạng 1 về permutation importance), nhưng bản chất nó là **vân tay hệ điều hành của máy tấn công**: 29.200 cho mọi cuộc tấn công năm 2017, 26.883 cho năm 2018, và -1 cho DDoS UDP năm 2019. Mô hình đang nhận diện *máy nào gửi gói tin*, chứ không phải *hành vi tấn công*. Đây là nguyên nhân chính khiến Bảng A đạt 0,999 nhưng Bảng B chỉ đạt 0,277.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 30 | 0 | 29.200 | 26.883 |

### 61. `min_seg_size_forward`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | -1 / 20 / 67.240.448 |
| Số giá trị phân biệt | 1.225 |
| Tỉ lệ bằng 0 | 1,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,820 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Kích thước segment nhỏ nhất quan sát được ở hướng thuận.

**Để làm gì:** Phản ánh độ dài header TCP: 20 byte nghĩa là không có tùy chọn, 32 hoặc 40 byte nghĩa là có tùy chọn. Vì vậy đây cũng là một dạng vân tay hệ điều hành, cần theo dõi khi diễn giải kết quả.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 20 | 20 | 40 | 32 |

## Khoảng cách giữa các gói (IAT)

### 8. `Bwd IAT Max`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 3 / 120.000.000 |
| Số giá trị phân biệt | 511.961 |
| Tỉ lệ bằng 0 | 41,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,807 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT lớn nhất hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 4 | 0 | 0 | 137.939 |

### 9. `Bwd IAT Mean`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 3 / 120.000.000 |
| Số giá trị phân biệt | 937.099 |
| Tỉ lệ bằng 0 | 41,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,807 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT trung bình hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 4 | 0 | 0 | 18 224.43 |

### 10. `Bwd IAT Min`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 2 / 120.000.000 |
| Số giá trị phân biệt | 150.304 |
| Tỉ lệ bằng 0 | 42,4% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,800 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT nhỏ nhất hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 3 | 0 | 0 | 10 |

### 11. `Bwd IAT Std`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 84.473.144 |
| Số giá trị phân biệt | 1.016.478 |
| Tỉ lệ bằng 0 | 65,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,747 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn IAT hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 36 966.47 |

### 12. `Bwd IAT Total`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 3 / 120.000.000 |
| Số giá trị phân biệt | 655.112 |
| Tỉ lệ bằng 0 | 41,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,807 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tổng IAT hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 4 | 0 | 0 | 375.471 |

### 23. `Flow IAT Max`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 1 / 36.566 / 120.000.000 |
| Số giá trị phân biệt | 701.481 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,880 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Khoảng nghỉ dài nhất giữa hai gói.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 31.797 | 1.176.773 | 47 | 100.096 |

### 24. `Flow IAT Mean`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.33 / 12 595.40 / 120.000.000 |
| Số giá trị phân biệt | 1.434.196 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,848 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Trung bình khoảng thời gian giữa hai gói liên tiếp, tính trên cả hai hướng.

**Để làm gì:** IAT đều đặn và cực nhỏ là dấu hiệu máy sinh lưu lượng; IAT không đều là dấu hiệu người dùng thật.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 16 204.67 | 176 372.86 | 47 | 8 718.09 |

### 25. `Flow IAT Min`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 4 / 120.000.000 |
| Số giá trị phân biệt | 136.243 |
| Tỉ lệ bằng 0 | 3,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,744 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Khoảng nghỉ ngắn nhất giữa hai gói.

**Để làm gì:** Dữ liệu gốc có 2.559 dòng mang giá trị âm do lỗi đồng hồ của CICFlowMeter; các dòng này đã bị loại bỏ ở bước 3.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 4 | 1 | 47 | 4 |

### 26. `Flow IAT Std`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 9 957.22 / 84.800.264 |
| Số giá trị phân biệt | 1.371.926 |
| Tỉ lệ bằng 0 | 32,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,853 |
| Hạng permutation importance * | **14/20** |

**Là gì:** Độ lệch chuẩn của IAT toàn luồng.

**Để làm gì:** Giá trị thấp đặc trưng cho công cụ tự động.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 1 762.67 | 448 284.38 | 0 | 20 466.04 |

### 29. `Fwd IAT Max`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 49 / 120.000.000 |
| Số giá trị phân biệt | 607.360 |
| Tỉ lệ bằng 0 | 21,7% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,907 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT lớn nhất hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 48 | 108.871 | 0 | 102.891 |

### 30. `Fwd IAT Mean`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 49 / 120.000.000 |
| Số giá trị phân biệt | 1.007.853 |
| Tỉ lệ bằng 0 | 21,7% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,907 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT trung bình hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 48 | 36.291 | 0 | 17 262.32 |

### 31. `Fwd IAT Min`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 3 / 120.000.000 |
| Số giá trị phân biệt | 123.048 |
| Tỉ lệ bằng 0 | 23,1% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,899 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** IAT nhỏ nhất hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 3 | 1 | 0 | 234 |

### 32. `Fwd IAT Std`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 84.602.928 |
| Số giá trị phân biệt | 990.499 |
| Tỉ lệ bằng 0 | 56,4% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,729 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn IAT hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 60 430.23 | 0 | 28 352.42 |

### 33. `Fwd IAT Total`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 49 / 120.000.000 |
| Số giá trị phân biệt | 735.853 |
| Tỉ lệ bằng 0 | 21,7% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,908 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tổng IAT hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 48 | 108.908 | 0 | 375.131 |

## Kích thước gói (theo hướng)

### 13. `Bwd Packet Length Max`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 102 / 19.530 |
| Số giá trị phân biệt | 4.809 |
| Tỉ lệ bằng 0 | 19,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,764 |
| Hạng permutation importance * | **13/20** |

**Là gì:** Payload lớn nhất trong một gói hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 110 | 0 | 6 | 976 |

### 14. `Bwd Packet Length Mean`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 92 / 5 800.50 |
| Số giá trị phân biệt | 145.179 |
| Tỉ lệ bằng 0 | 19,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,761 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Payload trung bình của gói hướng ngược.

**Để làm gì:** Trùng hoàn toàn với `Avg Bwd Segment Size` — cột đó đã bị loại bỏ.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 98.80 | 0 | 6 | 121.14 |

### 15. `Bwd Packet Length Min`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 2.896 |
| Số giá trị phân biệt | 591 |
| Tỉ lệ bằng 0 | 51,6% |
| Tách lớp tốt nhất (AUC đơn biến) | `DoS/DDoS` — 0,783 |
| Hạng permutation importance * | **16/20** |

**Là gì:** Payload nhỏ nhất trong một gói hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 6 | 0 | 6 | 0 |

### 16. `Bwd Packet Length Std`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 8 194.66 |
| Số giá trị phân biệt | 259.604 |
| Tỉ lệ bằng 0 | 65,4% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,732 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn payload hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 258.64 |

### 35. `Fwd Packet Length Max`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 46 / 64.440 |
| Số giá trị phân biệt | 5.264 |
| Tỉ lệ bằng 0 | 2,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,990 |
| Hạng permutation importance * | **4/20** |

**Là gì:** Payload lớn nhất trong một gói hướng thuận.

**Để làm gì:** Chạm trần MTU (~1460) ở DDoS khuếch đại; gần 0 ở quét cổng.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 45 | 350 | 0 | 640 |

### 36. `Fwd Packet Length Mean`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 42 / 11 217.03 |
| Số giá trị phân biệt | 90.156 |
| Tỉ lệ bằng 0 | 2,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,990 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Payload trung bình của gói hướng thuận.

**Để làm gì:** Trùng hoàn toàn với `Avg Fwd Segment Size` — cột đó đã bị loại bỏ.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 41.22 | 70.60 | 0 | 86.91 |

### 37. `Fwd Packet Length Min`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 6 / 2.325 |
| Số giá trị phân biệt | 1.147 |
| Tỉ lệ bằng 0 | 40,5% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,807 |
| Hạng permutation importance * | **19/20** |

**Là gì:** Payload nhỏ nhất trong một gói hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 6 | 6 | 0 | 0 |

### 38. `Fwd Packet Length Std`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 15 760.84 |
| Số giá trị phân biệt | 265.446 |
| Tỉ lệ bằng 0 | 58,2% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,822 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Độ lệch chuẩn payload hướng thuận.

**Để làm gì:** Bằng 0 nghĩa là mọi gói giống hệt nhau — dấu hiệu lưu lượng do công cụ tự động sinh ra.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 0 | 137.69 |

## Tốc độ

### 17. `Bwd Packets/s`

| | |
|---|---|
| Đơn vị | gói/giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 16.44 / 2.000.000 |
| Số giá trị phân biệt | 1.295.904 |
| Tỉ lệ bằng 0 | 17,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,969 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tốc độ gói hướng ngược.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 22.44 | 0 | 21 276.60 | 57.28 |

### 21. `Flow Bytes/s`

| | |
|---|---|
| Đơn vị | byte/giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.01 / 9 834.03 / 2.944.000.000 |
| Số giá trị phân biệt | 1.989.707 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,695 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tổng byte chia cho thời lượng luồng.

**Để làm gì:** Là nguồn sinh giá trị vô cực khi thời lượng bằng 0 — đã xử lý ở bước làm sạch. DDoS phản xạ năm 2019 đạt tới 2,9×10⁹ B/s, lệch sáu bậc so với năm 2017.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 7 263.19 | 6 200.52 | 139 534.89 | 12 249.73 |

### 27. `Flow Packets/s`

| | |
|---|---|
| Đơn vị | gói/giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.02 / 102.74 / 4.000.000 |
| Số giá trị phân biệt | 1.451.442 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,871 |
| Hạng permutation importance * | **6/20** |

**Là gì:** Tổng gói chia cho thời lượng luồng.

**Để làm gì:** Cùng nguồn sinh giá trị vô cực như cột trên.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 84.78 | 6.52 | 42 553.19 | 117.37 |

### 39. `Fwd Packets/s`

| | |
|---|---|
| Đơn vị | gói/giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0.01 / 54.89 / 4.000.000 |
| Số giá trị phân biệt | 1.422.389 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,861 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tốc độ gói hướng thuận.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 42.82 | 2.70 | 21 276.60 | 60.58 |

## Khác

### 18. `Down/Up Ratio`

| | |
|---|---|
| Đơn vị | tỉ lệ |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 1 / 156 |
| Số giá trị phân biệt | 47 |
| Tỉ lệ bằng 0 | 39,9% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,696 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tỉ lệ giữa số gói tải xuống và số gói tải lên.

**Để làm gì:** Duyệt web bình thường lệch mạnh về phía tải xuống; flood và quét cổng gần như chỉ đi một chiều.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 1 | 0 | 1 | 1 |

### 60. `act_data_pkt_fwd`

| | |
|---|---|
| Đơn vị | gói |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 1 / 108.273 |
| Số giá trị phân biệt | 847 |
| Tỉ lệ bằng 0 | 23,5% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,936 |
| Hạng permutation importance * | **15/20** |

**Là gì:** Số gói hướng thuận thực sự mang payload khác 0 byte.

**Để làm gì:** Phân biệt luồng chỉ bắt tay (quét cổng) với luồng truyền dữ liệu thật.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 1 | 2 | 0 | 16 |

## Thời lượng

### 22. `Flow Duration`

| | |
|---|---|
| Đơn vị | micro giây |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 1 / 48.279 / 120.000.000 |
| Số giá trị phân biệt | 1.247.788 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,886 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Khoảng thời gian từ gói tin đầu tiên đến gói tin cuối cùng của luồng.

**Để làm gì:** Đặc trưng nền tảng. Quét cổng và DDoS phản xạ sống rất ngắn (vài µs); brute force và kết nối bình thường kéo dài hàng giây.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 46 515.50 | 1.210.887 | 47 | 375.489 |

## Đếm gói & byte

### 55. `Total Backward Packets`

| | |
|---|---|
| Đơn vị | gói |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 2 / 157.388 |
| Số giá trị phân biệt | 1.698 |
| Tỉ lệ bằng 0 | 17,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,933 |
| Hạng permutation importance * | **8/20** |

**Là gì:** Số gói tin đi theo hướng ngược (máy chủ → máy khách).

**Để làm gì:** Thiếu phản hồi nghĩa là máy chủ không trả lời — dấu hiệu quét cổng hoặc flood.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 2 | 0 | 1 | 22 |

### 56. `Total Fwd Packets`

| | |
|---|---|
| Đơn vị | gói |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 1 / 2 / 112.141 |
| Số giá trị phân biệt | 1.319 |
| Tỉ lệ bằng 0 | 0,0% |
| Tách lớp tốt nhất (AUC đơn biến) | `BruteForce` — 0,938 |
| Hạng permutation importance * | **20/20** |

**Là gì:** Số gói tin đi theo hướng thuận (máy khách → máy chủ).

**Để làm gì:** Đo quy mô phiên. Luồng tấn công tự động thường có số gói rất nhỏ và lặp lại.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 2 | 4 | 1 | 22 |

### 57. `Total Length of Bwd Packets`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 160 / 399.000.000 |
| Số giá trị phân biệt | 68.704 |
| Tỉ lệ bằng 0 | 19,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,777 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Tổng payload của tất cả gói tin hướng ngược.

**Để làm gì:** Kết hợp với cột trên tạo tỉ lệ xuôi/ngược — phân biệt tải xuống với tải lên.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 174 | 0 | 6 | 2.665 |

### 58. `Total Length of Fwd Packets`

| | |
|---|---|
| Đơn vị | byte |
| Kiểu dữ liệu | float32 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 82 / 12.900.000 |
| Số giá trị phân biệt | 18.278 |
| Tỉ lệ bằng 0 | 2,8% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,996 |
| Hạng permutation importance * | **3/20** |

**Là gì:** Tổng payload của tất cả gói tin hướng thuận.

**Để làm gì:** Tách PortScan rất mạnh: gói quét gần như không mang payload.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 76 | 380 | 0 | 1.928 |

## Đặc trưng suy ra

### 62. `dst_port_class`

| | |
|---|---|
| Đơn vị | mã 0/1/2 |
| Kiểu dữ liệu | int8 |
| Nhỏ nhất / Trung vị / Lớn nhất | 0 / 0 / 2 |
| Số giá trị phân biệt | 3 |
| Tỉ lệ bằng 0 | 75,3% |
| Tách lớp tốt nhất (AUC đơn biến) | `PortScan` — 0,784 |
| Hạng permutation importance * | ngoài top 20 |

**Là gì:** Nhóm của cổng đích, **thay thế cho số cổng thô**: `0` là cổng hệ thống (dưới 1024), `1` là cổng đã đăng ký (1024–49151), `2` là cổng tạm thời (từ 49152).

**Để làm gì:** Cột `Destination Port` gốc đã bị **loại bỏ vì rò rỉ nghiêm trọng**: PortScan và DDoS của bộ 2017 tách được gần như hoàn hảo chỉ bằng số cổng, khiến mô hình ghi nhớ cấu hình phòng thí nghiệm thay vì học hành vi. Việc nhóm hóa giữ lại tín hiệu về loại dịch vụ mà không cho mô hình học thuộc từng cổng cụ thể.

Trung vị theo từng lớp:

| BENIGN | DoS/DDoS | PortScan | BruteForce |
|---|---|---|---|
| 0 | 0 | 1 | 0 |

## Nhãn và siêu dữ liệu

### 63. `label`

| | |
|---|---|
| Đơn vị | chuỗi |
| Kiểu dữ liệu | chuỗi |
| Số giá trị phân biệt | 4 |

**Là gì:** Nhãn mục tiêu, gồm bốn giá trị: `BENIGN`, `DDoS`, `PortScan`, `BruteForce`.

**Để làm gì:** **Đây là biến cần dự đoán (y).** Nhãn đã được hợp nhất từ các tên gọi khác nhau giữa ba bộ dữ liệu — ví dụ `FTP-Patator`, `SSH-Bruteforce` và `Web Attack – Brute Force` đều quy về `BruteForce`.

### 64. `attack_subtype`

| | |
|---|---|
| Đơn vị | chuỗi |
| Kiểu dữ liệu | chuỗi |
| Số giá trị phân biệt | 12 |

**Là gì:** Kiểu tấn công con bên trong mỗi lớp — ví dụ lớp `DoS/DDoS` gồm `HTTP Flood`, `SYN Flood`, `UDP Flood`, `Slowloris`, `Slow HTTP DoS`, `Reflection/Amplification`.

**Để làm gì:** **Không được dùng làm đặc trưng.** Đây là cột dành cho phân tích kết quả: nó cho phép trả lời câu hỏi *“mô hình bắt Slowloris tốt hơn hay HTTP Flood tốt hơn?”* thay vì chỉ có một chỉ số F1 chung cho cả lớp. Điều này quan trọng vì lớp `DoS/DDoS` gộp sáu kiểu tấn công có hành vi rất khác nhau — Slowloris giữ kết nối hàng phút trong khi UDP reflection chỉ sống khoảng một micro giây.

### 65. `source_dataset`

| | |
|---|---|
| Đơn vị | chuỗi |
| Kiểu dữ liệu | chuỗi |
| Số giá trị phân biệt | 3 |

**Là gì:** Bộ dữ liệu gốc: `2017`, `2018` hoặc `2019`.

**Để làm gì:** **Không được dùng làm đặc trưng.** Cột này dùng để chia tập cho đánh giá cross-dataset (Bảng B) và để phân tích riêng hiệu năng theo từng nguồn.

### 66. `source_file`

| | |
|---|---|
| Đơn vị | chuỗi |
| Kiểu dữ liệu | chuỗi |
| Số giá trị phân biệt | 10 |

**Là gì:** Tên file CSV gốc mà dòng này được đọc ra.

**Để làm gì:** **Không được dùng làm đặc trưng.** Dùng để truy ngược và gỡ lỗi.

### 67. `group_id`

| | |
|---|---|
| Đơn vị | uint64 |
| Kiểu dữ liệu | uint64 |
| Số giá trị phân biệt | 2.623.782 |

**Là gì:** Mã băm của toàn bộ vector 62 đặc trưng. Hai dòng trùng mã nghĩa là chúng giống hệt nhau ở mọi đặc trưng.

**Để làm gì:** **Không được dùng làm đặc trưng.** Bắt buộc truyền vào tham số `groups` của `StratifiedGroupKFold` để một vector không xuất hiện đồng thời ở cả tập huấn luyện lẫn tập kiểm tra. PortScan trùng lặp khoảng 99%, nên nếu chia ngẫu nhiên thì mọi chỉ số đo được đều vô nghĩa.

---

## Phụ lục A — 26 cột gốc đã bị loại bỏ

| Cột | Nhóm | Lý do loại bỏ |
|---|---|---|
| `Flow ID` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Source IP` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Source Port` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Destination IP` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Timestamp` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Unnamed: 0` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `SimillarHTTP` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Inbound` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Protocol` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Fwd Header Length.1` | Định danh | Định danh phòng thí nghiệm (địa chỉ IP, cổng nguồn, Flow ID, mốc thời gian) hoặc không tồn tại ở cả ba bộ dữ liệu. |
| `Destination Port` | Rò rỉ | Tách lớp gần như hoàn hảo, khiến mô hình ghi nhớ cấu hình phòng thí nghiệm. Đã thay bằng `dst_port_class`. |
| `Bwd PSH Flags` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Bwd URG Flags` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Fwd Avg Bytes/Bulk` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Fwd Avg Packets/Bulk` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Fwd Avg Bulk Rate` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Bwd Avg Bytes/Bulk` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Bwd Avg Packets/Bulk` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Bwd Avg Bulk Rate` | Hằng số | Chỉ có duy nhất một giá trị trên toàn bộ 4.179.318 dòng nên không mang thông tin. |
| `Avg Fwd Segment Size` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `Avg Bwd Segment Size` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `Subflow Fwd Packets` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `Subflow Fwd Bytes` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `Subflow Bwd Packets` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `Subflow Bwd Bytes` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |
| `CWE Flag Count` | Trùng lặp | Là bản sao từ 99,99% trở lên của một cột khác, chỉ làm loãng feature importance. |

## Phụ lục B — Đối chiếu tên cột giữa ba bộ dữ liệu

Tên chuẩn được lấy theo **CIC-IDS2017**. Bộ 2019 đã trùng 100% nên không cần đổi tên; chỉ bộ 2018 dùng tên viết tắt.

| Tên trong bộ 2018 | Tên chuẩn (2017 và 2019) |
|---|---|
| `ACK Flag Cnt` | `ACK Flag Count` |
| `Bwd Blk Rate Avg` | `Bwd Avg Bulk Rate` |
| `Bwd Byts/b Avg` | `Bwd Avg Bytes/Bulk` |
| `Bwd Header Len` | `Bwd Header Length` |
| `Bwd IAT Tot` | `Bwd IAT Total` |
| `Bwd Pkt Len Max` | `Bwd Packet Length Max` |
| `Bwd Pkt Len Mean` | `Bwd Packet Length Mean` |
| `Bwd Pkt Len Min` | `Bwd Packet Length Min` |
| `Bwd Pkt Len Std` | `Bwd Packet Length Std` |
| `Bwd Pkts/b Avg` | `Bwd Avg Packets/Bulk` |
| `Bwd Pkts/s` | `Bwd Packets/s` |
| `Bwd Seg Size Avg` | `Avg Bwd Segment Size` |
| `Dst Port` | `Destination Port` |
| `ECE Flag Cnt` | `ECE Flag Count` |
| `FIN Flag Cnt` | `FIN Flag Count` |
| `Flow Byts/s` | `Flow Bytes/s` |
| `Flow Pkts/s` | `Flow Packets/s` |
| `Fwd Act Data Pkts` | `act_data_pkt_fwd` |
| `Fwd Blk Rate Avg` | `Fwd Avg Bulk Rate` |
| `Fwd Byts/b Avg` | `Fwd Avg Bytes/Bulk` |
| `Fwd Header Len` | `Fwd Header Length` |
| `Fwd IAT Tot` | `Fwd IAT Total` |
| `Fwd Pkt Len Max` | `Fwd Packet Length Max` |
| `Fwd Pkt Len Mean` | `Fwd Packet Length Mean` |
| `Fwd Pkt Len Min` | `Fwd Packet Length Min` |
| `Fwd Pkt Len Std` | `Fwd Packet Length Std` |
| `Fwd Pkts/b Avg` | `Fwd Avg Packets/Bulk` |
| `Fwd Pkts/s` | `Fwd Packets/s` |
| `Fwd Seg Size Avg` | `Avg Fwd Segment Size` |
| `Fwd Seg Size Min` | `min_seg_size_forward` |
| `Init Bwd Win Byts` | `Init_Win_bytes_backward` |
| `Init Fwd Win Byts` | `Init_Win_bytes_forward` |
| `PSH Flag Cnt` | `PSH Flag Count` |
| `Pkt Len Max` | `Max Packet Length` |
| `Pkt Len Mean` | `Packet Length Mean` |
| `Pkt Len Min` | `Min Packet Length` |
| `Pkt Len Std` | `Packet Length Std` |
| `Pkt Len Var` | `Packet Length Variance` |
| `Pkt Size Avg` | `Average Packet Size` |
| `RST Flag Cnt` | `RST Flag Count` |
| `SYN Flag Cnt` | `SYN Flag Count` |
| `Subflow Bwd Byts` | `Subflow Bwd Bytes` |
| `Subflow Bwd Pkts` | `Subflow Bwd Packets` |
| `Subflow Fwd Byts` | `Subflow Fwd Bytes` |
| `Subflow Fwd Pkts` | `Subflow Fwd Packets` |
| `Tot Bwd Pkts` | `Total Backward Packets` |
| `Tot Fwd Pkts` | `Total Fwd Packets` |
| `TotLen Bwd Pkts` | `Total Length of Bwd Packets` |
| `TotLen Fwd Pkts` | `Total Length of Fwd Packets` |
| `URG Flag Cnt` | `URG Flag Count` |

_Tổng cộng 50 cặp đổi tên. Bảng map đầy đủ nằm trong `src/schema.py`, biến `RENAME_2018`._

## Phụ lục C — Độ phủ so với phạm vi đề tài

Đối chiếu phạm vi nhận diện tấn công đã khai báo với dữ liệu thực sự có. Các mục ❌ phải được nêu thẳng trong phần *Giới hạn nghiên cứu* của khoá luận.

| Phạm vi khai báo | Dữ liệu tương ứng | Trạng thái |
|---|---|---|
| **DoS/DDoS** — SYN Flood | 2019 `Syn` | ✅ |
| **DoS/DDoS** — UDP Flood | 2019 `UDP`, `UDP-lag`, `DrDoS_UDP`, `TFTP` | ✅ |
| **DoS/DDoS** — HTTP Flood | 2017 `DDoS` (LOIC), `DoS Hulk`, `DoS GoldenEye` | ✅ |
| **DoS/DDoS** — Slowloris | 2017 `DoS slowloris`, `DoS Slowhttptest` | ✅ |
| **DoS/DDoS** — ICMP Flood | — | ❌ không có trong cả ba bộ |
| **Port Scan** — TCP SYN / TCP Connect | 2017 `PortScan` (nmap) | ✅ |
| **Port Scan** — FIN/NULL/XMAS, UDP Scan | gộp chung nhãn `PortScan` | ⚠️ có nhưng không tách được |
| **Port Scan** — quét dải mạng | cần Destination IP | ❌ dữ liệu đã bị tước IP |
| **Brute Force** — SSH | 2017 `SSH-Patator`, 2018 `SSH-Bruteforce` | ✅ |
| **Brute Force** — FTP | 2017 `FTP-Patator` | ✅ |
| **Brute Force** — HTTP Form Login | 2017 `Web Attack – Brute Force` | ⚠️ còn rất ít sau lọc |
| **Brute Force** — RDP, VPN, SMB | — | ❌ không có trong cả ba bộ |

> **Vì sao lớp `DoS/DDoS` gộp cả DoS một nguồn lẫn DDoS phân tán:** phạm vi đề tài định nghĩa nhóm này là *“DDoS / DoS”* và nêu đích danh Slowloris cùng HTTP Flood — đó là các tấn công từ **một nguồn**. Vì vậy `DoS Hulk`, `DoS GoldenEye`, `DoS slowloris` và `DoS Slowhttptest` của bộ 2017 được xếp cùng lớp với DDoS phân tán. Hệ quả cần lưu ý: lớp này chứa sáu kiểu tấn công có hành vi rất khác nhau, nên hãy dùng cột `attack_subtype` để báo cáo hiệu năng chi tiết thay vì chỉ một chỉ số chung.

## Phụ lục D — Năm cảnh báo khi sử dụng bộ dữ liệu này

**1. `Init_Win_bytes_forward` là đặc trưng mạnh nhất nhưng cũng nguy hiểm nhất.** Nó là vân tay hệ điều hành của máy tấn công (29.200 ở bộ 2017, 26.883 ở bộ 2018, -1 ở DDoS UDP bộ 2019) chứ không phải hành vi tấn công. Nếu muốn kết quả có khả năng tổng quát hóa, hãy thử loại bỏ nó cùng với `Init_Win_bytes_backward` và `min_seg_size_forward`, rồi đo lại.

**2. Luôn chia tập theo `group_id`.** Lớp PortScan có 158.253 dòng nhưng chỉ chứa 1.963 vector phân biệt. Chia ngẫu nhiên sẽ khiến cùng một vector nằm ở cả tập huấn luyện lẫn tập kiểm tra.

**3. Lớp `PortScan` chỉ tồn tại trong bộ 2017.** Bộ 2018 (ngày 14-02) chỉ có brute force, bộ 2019 thuần DDoS. Vì vậy không có bằng chứng nào về khả năng tổng quát hóa của lớp này sang mạng khác.

**4. Lớp `DDoS` có hai chế độ tách biệt.** Bộ 2017 là HTTP/TCP flood, bộ 2019 là UDP reflection. Hai chế độ này cách nhau nhiều bậc độ lớn về `Flow Bytes/s` và `Flow Duration`, nên mô hình học hai khái niệm riêng chứ không phải một khái niệm DDoS thống nhất.

**5, Dùng macro-F1, không dùng accuracy,** Lớp BENIGN chiếm 75,3% tổng số dòng nên accuracy luôn đẹp một cách giả tạo.