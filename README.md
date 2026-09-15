# 🎓 KHÓA LUẬN TỐT NGHIỆP ĐẠI HỌC (2026)

## NGHIÊN CỨU ỨNG DỤNG HỌC MÁY TRONG GIÁM SÁT VÀ PHÁT HIỆN BẤT THƯỜNG TRÊN HỆ THỐNG MẠNG DOANH NGHIỆP
> **English Title:** *Research and Application of Machine Learning in Network Anomaly Detection and Monitoring for Enterprise Systems*

---

## 🏛️ THÔNG TIN CHUNG
* **Cơ sở đào tạo:** Trường Đại học Mở Hà Nội (HOU)
* **Khoa:** Công nghệ Thông tin
* **Chuyên ngành:** Mạng và An toàn thông tin
* **Giảng viên hướng dẫn:** ThS. Nguyễn Thành Huy
* **Thời gian thực hiện:** 2026

---

## 👥 THÀNH VIÊN NHÓM & PHÂN CÔNG CÔNG VIỆC

| STT | Họ và tên | Mã sinh viên | Vai trò & Nhiệm vụ trọng tâm |
| :---: | :--- | :---: | :--- |
| **1** | **Nguyễn Huy Hoàng** | **2310A04** | • Thiết kế kiến trúc Backend & Cơ sở dữ liệu (PostgreSQL).<br>• Xây dựng dịch vụ suy luận mô hình (Inference Service) bằng FastAPI.<br>• Xây dựng bộ gom cụm cảnh báo (**Event Correlation**) & gửi cảnh báo (Telegram/Email).<br>• Thiết kế hệ thống RESTful API & WebSocket phục vụ Dashboard giám sát.<br>• Tham gia viết báo cáo khóa luận. |
| **2** | **Đoàn Lê Đức Anh** | **2310A04** | • Xây dựng môi trường mạng Lab mô phỏng (VLAN, DMZ, pfSense Firewall).<br>• Xây dựng kịch bản & thực thi tấn công thử nghiệm (`hping3`, `nmap`, `hydra`).<br>• Triển khai bắt gói tin, thu thập và gán nhãn dữ liệu lưu lượng thực nghiệm (`.pcap`).<br>• Tham gia viết báo cáo khóa luận. |
| **3** | **Phùng Ngọc Linh** | **2310A02** | • Thu thập, làm sạch và xử lý các tập dữ liệu mạng (CICIDS2017, CSE-CIC-IDS2018, Lab traffic).<br>• Trích xuất đặc trưng luồng mạng bằng **CICFlowMeter**.<br>• Khám phá dữ liệu (EDA), loại bỏ đặc trưng rò rỉ nhãn (**Data Leakage prevention**) & chọn lọc đặc trưng tối ưu.<br>• Xử lý mất cân bằng dữ liệu (SMOTE/Downsampling) và chuẩn hóa dữ liệu đầu vào.<br>• Tham gia viết báo cáo khóa luận. |
| **4** | **Nguyễn Văn Khải** | **2310A04** | • Huấn luyện các mô hình học máy (Random Forest, XGBoost, LightGBM, MLP, Isolation Forest).<br>• Tinh chỉnh siêu tham số (Hyperparameter Tuning), đánh giá hiệu năng (F1-macro, Recall, FPR, AUC-ROC).<br>• Đánh giá kiểm chứng chéo và phân tích mức độ quan trọng của đặc trưng (**Feature Importance**).<br>• Đóng gói mô hình và scaler tối ưu (`.joblib`) phục vụ triển khai.<br>• Tham gia viết báo cáo khóa luận. |
| **5** | **Trương Nguyễn Đức Anh** | **2210A03** | • Thiết kế UI/UX và xây dựng Frontend Dashboard giám sát an ninh bằng **React + Vite + Tailwind CSS**.<br>• Trực quan hóa dữ liệu lưu lượng mạng, danh sách cảnh báo, biểu đồ thống kê an ninh mạng.<br>• Đóng gói và triển khai toàn bộ hệ thống bằng **Docker & Docker Compose**.<br>• Xây dựng checklist kiểm thử chức năng và đo độ trễ hệ thống (Detection Latency).<br>• Tham gia viết báo cáo khóa luận. |

---

## 🎯 BÀI TOÁN & PHẠM VI NGHIÊN CỨU

Hệ thống tập trung vào bài toán **phân loại đa lớp 4 nhãn (Multi-class Classification)** trên các đặc trưng luồng mạng (Flow-based Statistics):
$$\mathcal{Y} = \{\text{BENIGN}, \text{DoS/DDoS}, \text{PortScan}, \text{BruteForce}\}$$

### 1. Phạm vi nhận diện tấn công (In-Scope)
* **DoS / DDoS:** SYN Flood, UDP Flood, ICMP Flood, HTTP Flood (Hulk, GoldenEye, LOIC, HOIC), Slowloris, SlowHTTPTest, Reflection/Amplification (DNS, NTP, SNMP, LDAP, MSSQL, TFTP).
* **Port Scan (Trinh sát mạng):** TCP SYN Scan, TCP Connect, FIN/NULL/XMAS, UDP Scan, Host Discovery.
* **Brute Force (Vét cạn mật khẩu):** Tấn công các dịch vụ xác thực SSH, FTP, HTTP Form Login.

### 2. Giới hạn ngoài phạm vi (Out-of-Scope)
* Không phân tích mã độc ở mức payload tệp tin (không quét nhị phân).
* Không giải mã lưu lượng mã hóa TLS/HTTPS (chỉ phân tích metadata của luồng).
* Không can thiệp ngắt kết nối tự động (IPS) mà tập trung vào **Giám sát & Cảnh báo an ninh mạng (IDS / Monitoring)**.

---

## 📊 BỘ DỮ LIỆU HỢP NHẤT (UNIFIED DATASET SPECIFICATION)

Dự án đã chuẩn hóa và hợp nhất thành công **3.305.401 dòng luồng mạng** từ 3 bộ chuẩn quốc tế (cùng không gian đặc trưng CICFlowMeter) phục vụ huấn luyện và kiểm định:

| Nguồn | Số dòng gốc | Sau làm sạch & lọc | Tỷ lệ giữ lại | Đóng góp chính |
| :--- | ---:| ---:| :---: | :--- |
| **CICIDS2017** | 2.827.876 | **2.467.237** | 87.2% | Lớp nền tảng: Đủ 4 lớp (BENIGN, DDoS, PortScan, BruteForce) |
| **CSE-CIC-IDS2018** | 1.048.575 | **591.454** | 56.4% | Làm giàu lớp BruteForce (SSH/FTP) và BENIGN quy mô lớn |
| **CIC-DDoS2019** | 300.000 | **246.710** | 82.2% | Bổ sung các biến thể DDoS phản xạ/khuếch đại (NTP, DNS, LDAP...) |
| **TỔNG HỢP NHẤT** | **4.176.451** | **3.305.401** | **79.1%** | **62 đặc trưng đầu vào + 5 cột siêu dữ liệu** |

### 1. Phân bố 4 lớp mục tiêu trong tập hợp nhất
* **`BENIGN`**: 2.488.400 dòng (75.3%)
* **`DoS/DDoS`**: 553.889 dòng (16.8%)
* **`PortScan`**: 158.253 dòng (4.8%)
* **`BruteForce`**: 104.859 dòng (3.2%)

### 2. Xử lý rò rỉ dữ liệu (Data Leakage) & Trùng lặp
* **Loại bỏ 10 cột rò rỉ / định danh:** `Flow ID`, `Source IP`, `Source Port`, `Destination IP`, `Timestamp`, `Unnamed: 0`, `SimillarHTTP`, `Inbound`, `Protocol`, `Fwd Header Length.1`.
* **Kỹ thuật Cổng dịch vụ (`dst_port_class`):** Thay vì giữ số cổng cụ thể (dẫn tới mô hình "học vẹt" số port), cổng được phân nhóm theo lớp dịch vụ chuẩn.
* **Loại bỏ 8 cột hằng số** (toàn bộ giá trị 0) và **7 cột dư thừa** hoàn toàn về mặt toán học.
* **Cơ chế `group_id` & `StratifiedGroupKFold`:** Khắc phục tình trạng PortScan có tỷ lệ trùng lặp lên tới 98.8% khi bỏ IP/Port. Toàn bộ các dòng thuộc cùng một phiên quét/tấn công được nhóm vào chung một `group_id` để đảm bảo **tuyệt đối không bị rò rỉ chéo giữa tập Train và Test**.

---

## 📈 KẾT QUẢ THỰC NGHIỆM ĐỐI CHỨNG (BENCHMARK RESULTS)

Nhóm đã thiết lập 2 giao thức đánh giá nghiêm ngặt, chỉ ra sự khác biệt giữa mô hình lý thuyết và thực tế:

### Giao thức A — Đánh giá trong cùng phân bố (Pooled Group-Aware Split 70/15/15)
*Toàn bộ 3 nguồn được gộp lại và chia nhóm theo `group_id` (train: 2.26M / test: 452K dòng):*

| Mô hình | Thời gian train | Macro F1 (Val) | Macro F1 (Test) | Độ chính xác (Accuracy) |
| :--- | :---: | :---: | :---: | :---: |
| **Random Forest (100 trees)** | 169s | **0.9983** | **0.9991** | **99.96%** |
| **HistGradientBoosting** | 72s | 0.9934 | 0.9989 | 99.94% |
| **Decision Tree (max_depth=8)** | 143s | 0.9943 | 0.9958 | 99.83% |
| **Logistic Regression** | 28s | 0.9141 | 0.9246 | 92.46% |

### Giao thức B — Đánh giá tổng quát hóa ngoài phân bố (Cross-Dataset Evaluation)
*Mô hình huấn luyện trên môi trường mạng này nhưng kiểm thử trên môi trường mạng hoàn toàn xa lạ:*
* **Train 2017 $\rightarrow$ Test 2018 (BENIGN & BruteForce):** Macro F1 = **0.4564**
* **Train 2017 $\rightarrow$ Test 2019 (BENIGN & DDoS):** Macro F1 = **0.0013**
* **Độ chênh lệch hiệu năng giữa Bảng A và B:** **+0.7224**
> 💡 *Ý nghĩa nghiên cứu quan trọng:* Chứng minh các mô hình học máy bị sụt giảm hiệu năng nghiêm trọng do hiện tượng "học thuộc lòng" đặc trưng của một testbed cố định. Đây là cơ sở thực tiễn khẳng định hệ thống mạng doanh nghiệp cần có cơ chế giám sát thực tế và cập nhật dữ liệu liên tục.

---

## 🏗️ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống áp dụng kiến trúc **Xử lý theo lô định kỳ (Micro-batch 5–10 giây)** kết hợp **Gom cụm sự kiện (Event Correlation)** nhằm đảm bảo khả năng giám sát gần thời gian thực (Near Real-time) và loại bỏ hoàn toàn hiện tượng quá tải cảnh báo (**Alert Fatigue**):

```
[Switch SPAN / Mirror / Máy ảo Lab]
               │
               ▼
   [Bộ thu thập: tcpdump / Zeek]
               │ (pcap định kỳ 5-10s)
               ▼
   [Bộ trích xuất: CICFlowMeter]
               │ (Vector 62 đặc trưng)
               ▼
   [Dịch vụ suy luận: FastAPI + Model Engine]
               │ (Nhãn dự đoán + Độ tin cậy)
               ▼
   [Bộ gom cụm cảnh báo: Event Correlation Engine]
         │                              │
         ├──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
[PostgreSQL Database]       [Telegram Bot / Email]          [React Dashboard UI]
(Lưu luồng, incident, log)     (Thông báo tức thời)       (Biểu đồ & chi tiết sự kiện)
```

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
KhoaLuan/
├── README.md                    # Bản mô tả tổng quan dự án
├── .gitignore                   # Cấu hình loại bỏ dữ liệu nặng (.parquet, .csv, cache)
├── docs/                        # Tài liệu đặc tả và đề cương khóa luận
│   ├── DATA_CONTRACT_v1.md      # Hợp đồng dữ liệu đóng băng (Schema & Quy tắc)
│   ├── DE_CUONG_CHI_TIET.md     # Toàn văn đề cương chi tiết
│   └── DeCuong_ChinhThuc.docx   # Đề cương chính thức từ GVHD
├── reports/                     # Báo cáo kỹ thuật & Từ điển dữ liệu
│   ├── COLUMNS.md               # Từ điển chi tiết 67 cột dữ liệu (1.559 dòng)
│   ├── 01_schema_audit.md       # Báo cáo kiểm định schema 3 bộ dữ liệu
│   ├── 02_median_pivot.md       # Phân tích trung vị đặc trưng theo nhãn
│   ├── 03_build.md              # Báo cáo quy trình dựng dataset hợp nhất
│   ├── 04_quality.md            # Báo cáo kiểm định chất lượng dữ liệu & rò rỉ
│   ├── 05_pooled.md             # Báo cáo kết quả thử nghiệm Giao thức A (Pooled)
│   └── 06_cross.md              # Báo cáo kết quả thử nghiệm Giao thức B (Cross-dataset)
├── data/                        # Quản lý tập dữ liệu (Lưu nội bộ, không push lên Git)
│   ├── raw/                     # Dữ liệu gốc (.csv, .pcap)
│   └── processed/               # Dữ liệu hợp nhất đã làm sạch
│       ├── unified.parquet      # Toàn bộ 3.3M dòng (315 MB)
│       ├── unified_2017.parquet # Dữ liệu 2017 sạch (242 MB)
│       ├── unified_2018.parquet # Dữ liệu 2018 sạch (66 MB)
│       ├── unified_2019.parquet # Dữ liệu 2019 sạch (7.7 MB)
│       └── ALL.csv              # File csv tổng hợp (1.04 GB)
├── lab/                         # Cấu hình mạng Lab ảo & kịch bản tấn công
│   ├── network_topology/
│   └── attack_scripts/
├── notebooks/                   # Jupyter Notebooks nghiên cứu & huấn luyện mô hình
├── ml_engine/                   # Mã nguồn huấn luyện, tiền xử lý và đóng gói model
│   ├── extractors/              # Script gọi trích xuất đặc trưng
│   ├── preprocessors/           # Scaler, feature selection
│   └── saved_models/            # File model tối ưu (.joblib)
├── backend/app/                 # Mã nguồn FastAPI Backend & Event Correlation
└── frontend/src/                # Mã nguồn Dashboard React giám sát an ninh
```

---

## 💻 HƯỚNG DẪN SỬ DỤNG NHANH DỮ LIỆU ĐỂ HUẤN LUYỆN (QUICKSTART)

Các thành viên phụ trách huấn luyện mô hình (Khải, Hoàng) có thể nạp dữ liệu sạch trực tiếp từ file Parquet cực nhanh:

```python
import pandas as pd

# Đọc 3.3 triệu dòng đã tối ưu kiểu float32 chỉ trong vài giây
df = pd.read_parquet('data/processed/unified.parquet')

# Tách riêng 62 đặc trưng và nhãn mục tiêu
META_COLS = ['label', 'attack_subtype', 'source_dataset', 'source_file', 'group_id']
X = df.drop(columns=META_COLS)  # 62 đặc trưng mạng
y = df['label']                 # Nhãn: BENIGN, DoS/DDoS, PortScan, BruteForce
groups = df['group_id']         # Bắt buộc dùng cho StratifiedGroupKFold
```

---

## 🚀 QUY TẮC GIT WORKFLOW CHO NHÓM

1. **Nhánh `main` là nhánh đóng băng:** Tuyệt đối không commit hoặc push trực tiếp vào `main`.
2. **Nhánh `Demo` là nhánh tích hợp chung:** Mọi nhánh tính năng mới bắt buộc phải tách ra từ `Demo` (`git checkout -b feature/<tên-tính-năng> Demo`).
3. **Tuyệt đối không commit dữ liệu lớn lên Git:** Dữ liệu nặng (`.parquet`, `.csv`, `.pcap`) đã được đưa vào `.gitignore` và chia sẻ nội bộ qua link Cloud Drive chung của nhóm.
