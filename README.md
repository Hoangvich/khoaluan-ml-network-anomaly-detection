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
$$\mathcal{Y} = \{\text{BENIGN}, \text{DDOS}, \text{PORTSCAN}, \text{BRUTEFORCE}\}$$

### 1. Phạm vi nhận diện tấn công (In-Scope)
* **DDoS / DoS:** SYN Flood, UDP Flood, ICMP Flood, HTTP Flood, Slowloris.
  * *Dấu hiệu:* Tăng vọt số lượng luồng trong cửa sổ ngắn, tỉ lệ gói SYN cao bất thường chưa hoàn tất bắt tay 3 bước, nhiều IP nguồn hướng về 1 IP đích.
* **Port Scan (Trinh sát mạng):** TCP SYN Scan, TCP Connect, FIN/NULL/XMAS, UDP Scan, quét dải mạng (Host Discovery).
  * *Dấu hiệu:* 1 IP nguồn kết nối tới hàng loạt cổng/địa chỉ đích khác nhau, thời lượng luồng cực ngắn, tỉ lệ gói cờ RST cao, kích thước gói nhỏ.
* **Brute Force (Vét cạn mật khẩu):** Tấn công các dịch vụ xác thực SSH, RDP, FTP, HTTP Form Login, VPN, SMB.
  * *Dấu hiệu:* Kết nối lặp lại liên tục tới cổng dịch vụ xác thực cố định, kích thước gói đồng dạng, tần suất xuất hiện đều đặn với tỷ lệ phản hồi lỗi cao.

### 2. Giới hạn ngoài phạm vi (Out-of-Scope)
* Không phân tích mã độc ở mức payload tệp tin (không quét nhị phân).
* Không giải mã lưu lượng mã hóa TLS/HTTPS (chỉ phân tích metadata của luồng).
* Không can thiệp ngắt kết nối tự động (IPS) mà tập trung vào **Giám sát & Cảnh báo an ninh mạng (IDS / Monitoring)**.

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
               │ (Vector đặc trưng luồng)
               ▼
   [Dịch vụ suy luận: FastAPI + Model Engine]
               │ (Nhãn dự đoán + Độ tin cậy)
               ▼
   [Bộ gom cụm cảnh báo: Event Correlation]
         │                              │
         ├──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
[PostgreSQL Database]       [Telegram Bot / Email]          [React Dashboard UI]
(Lưu luồng, incident, log)     (Thông báo tức thời)       (Biểu đồ & chi tiết sự kiện)
```

---

## 🧩 PHÂN RÃ CÁC MODULE CHÍNH (M1 - M8)

* **M1: Tổng quan & Nghiên cứu lý thuyết:** Phân tích đặc trưng luồng mạng, tấn công mạng doanh nghiệp, cơ chế Signature vs Anomaly-based.
* **M2: Xây dựng Lab mạng doanh nghiệp:** Thiết lập pfSense, 3 phân vùng mạng (LAN, Server, DMZ), kịch bản tấn công thực nghiệm và bắt file `.pcap`.
* **M3: Xử lý dữ liệu luồng mạng:** Đồng nhất đặc trưng bằng CICFlowMeter, loại trừ data leakage (loại bỏ IP, Port, Timestamp khỏi tập train), chuẩn hóa scaler và cân bằng lớp (SMOTE).
* **M4: Huấn luyện & Đánh giá mô hình:** So sánh Random Forest, XGBoost, LightGBM, MLP; đánh giá F1-macro, False Positive Rate (FPR), Confusion Matrix và Feature Importance.
* **M5: Dịch vụ suy luận (Model Serving):** Đóng gói pipeline dự đoán hiệu năng cao với FastAPI.
* **M6: Backend & Event Correlation:** Quản lý cơ sở dữ liệu PostgreSQL, giải thuật gom cụm luồng cùng loại theo khung thời gian thành 1 Incident an ninh, gửi thông báo Telegram.
* **M7: Frontend Dashboard:** Giao diện điều hành an ninh SOC trực quan, xem chi tiết luồng, phân tích nguyên nhân cảnh báo.
* **M8: Đóng gói Docker, Kiểm thử & Đánh giá:** Triển khai Docker Compose toàn hệ thống, đo kiểm độ trễ phát hiện (Detection Latency) và tài nguyên tiêu thụ.

---

## 🛠️ CÔNG NGHỆ VÀ CÔNG CỤ SỬ DỤNG

* **Môi trường mô phỏng:** VMware Workstation, pfSense Firewall, Ubuntu Server, Windows Server.
* **Công cụ an ninh & bắt gói:** `tcpdump`, `Wireshark`, `Zeek`, `CICFlowMeter`, `nmap`, `hping3`, `hydra`.
* **Khoa học dữ liệu & Học máy:** Python, Pandas, NumPy, Scikit-learn, XGBoost, LightGBM, Imbalanced-learn, Joblib.
* **Backend & API:** Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic.
* **Cơ sở dữ liệu:** PostgreSQL.
* **Frontend:** React 18, Vite, Tailwind CSS, Lucide Icons, Recharts.
* **DevOps & Triển khai:** Docker, Docker Compose, Git / GitHub.

---

## 📂 CẤU TRÚC THƯ MỤC DỰ ÁN

```
KhoaLuan/
├── .github/                # GitHub workflows / CI/CD (nếu có)
├── docs/                   # Tài liệu đề cương, báo cáo, tài liệu thiết kế
│   ├── DeCuong_ChinhThuc.docx
│   └── DE_CUONG_CHI_TIET.md
├── lab/                    # Cấu hình mạng Lab ảo, kịch bản tấn công, script pcap
│   ├── network_topology/
│   └── attack_scripts/
├── data/                   # Quản lý tập dữ liệu (không đẩy dữ liệu nặng lên git)
│   ├── raw/                # File pcap thô, dataset gốc
│   └── processed/          # File csv sau khi trích xuất đặc trưng
├── notebooks/              # Jupyter Notebooks nghiên cứu EDA & thử nghiệm mô hình
│   ├── 01_eda_and_cleaning.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_evaluation_and_explainability.ipynb
├── ml_engine/              # Source code huấn luyện & đóng gói model
│   ├── extractors/         # Trình gọi CICFlowMeter
│   ├── preprocessors/      # Scaler, feature selector
│   └── saved_models/       # File model đã đóng gói (.joblib)
├── backend/                # Source code FastAPI Backend & Event Correlation
│   ├── app/
│   │   ├── api/            # Router endpoints
│   │   ├── core/           # Config, logging
│   │   ├── db/             # Models & Database connection
│   │   ├── services/       # Inference service, Correlation engine, Telegram alerter
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Source code Dashboard React
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml      # File cấu hình khởi chạy toàn bộ hệ thống
└── README.md
```

---

## 🚀 HƯỚNG DẪN DÀNH CHO THÀNH VIÊN NHÓM (GIT WORKFLOW)

1. **Clone repository về máy:**
   ```bash
   git clone https://github.com/Hoangvich/khoaluan-ml-network-anomaly-detection.git
   cd khoaluan-ml-network-anomaly-detection
   ```
2. **Tạo nhánh làm việc tương ứng với phân công:**
   * Đức Anh (Lab): `git checkout -b feature/lab-simulation`
   * Linh (Data): `git checkout -b feature/data-pipeline`
   * Khải (Model): `git checkout -b feature/model-training`
   * Hoàng (Backend/API): `git checkout -b feature/backend-inference`
   * Đức Anh (Frontend): `git checkout -b feature/frontend-dashboard`
3. **Quy tắc làm việc:**
   * Không commit trực tiếp vào nhánh `main`.
   * Không commit file dữ liệu nặng (`.pcap`, `.csv` hàng trăm MB, model nặng) lên Git (dùng link Google Drive/OneDrive chung của nhóm).
   * Tạo Pull Request (PR) khi hoàn thành chức năng để cả nhóm cùng review.
