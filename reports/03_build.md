# Buoc 3 - Dung dataset thong nhat

- Tong: **3,305,401 dong**
- Cot dau vao: **62** (61 feature so + `dst_port_class`)
- Group phan biet: **2,623,782**

## Dem theo tung giai doan

| Lop | Nguon | 1. chon lop | 2. bo Inf/NaN | 3. loc rac | 4. bo gia tri bat kha thi | Giu lai |
|---|---|---:|---:|---:|---:|---:|
| BENIGN | 2017 | 2,273,097 | 2,271,320 | 1,992,978 | 1,990,409 | 87.6% |
| BENIGN | 2018 | 667,626 | 663,808 | 497,636 | 497,636 | 74.5% |
| BENIGN | 2019 | 487 | 480 | 359 | 355 | 72.9% |
| DoS/DDoS | 2017 | 380,688 | 379,737 | 307,709 | 307,534 | 80.8% |
| DoS/DDoS | 2019 | 299,513 | 290,273 | 282,650 | 246,355 | 82.3% |
| PortScan | 2017 | 158,930 | 158,804 | 158,253 | 158,253 | 99.6% |
| BruteForce | 2017 | 15,342 | 15,339 | 11,047 | 11,041 | 72.0% |
| BruteForce | 2018 | 380,949 | 380,943 | 93,818 | 93,818 | 24.6% |

## Tong theo lop

| Lop | Dong | Group phan biet | Ti le trung lap |
|---|---:|---:|---:|
| BENIGN | 2,488,400 | 2,127,038 | 14.5% |
| DoS/DDoS | 553,889 | 392,123 | 29.2% |
| PortScan | 158,253 | 1,963 | 98.8% |
| BruteForce | 104,859 | 102,857 | 1.9% |

## Theo kieu tan cong con (`attack_subtype`)

| Lop | Kieu tan cong | Nguon | Dong | Group phan biet |
|---|---|---|---:|---:|
| BENIGN | - | 2017 | 1,990,409 | 1,685,227 |
| BENIGN | - | 2018 | 497,636 | 441,556 |
| BENIGN | - | 2019 | 355 | 353 |
| DoS/DDoS | HTTP Flood | 2017 | 172,703 | 172,407 |
| DoS/DDoS | HTTP Flood (LOIC) | 2017 | 128,006 | 127,995 |
| DoS/DDoS | Reflection/Amplification | 2019 | 126,562 | 29,341 |
| DoS/DDoS | UDP Flood | 2019 | 100,258 | 52,366 |
| DoS/DDoS | SYN Flood | 2019 | 19,534 | 4,610 |
| DoS/DDoS | Slowloris | 2017 | 4,149 | 3,730 |
| DoS/DDoS | Slow HTTP DoS | 2017 | 2,676 | 2,405 |
| DoS/DDoS | HTTP Flood | 2019 | 1 | 1 |
| PortScan | TCP SYN/Connect Scan | 2017 | 158,253 | 1,963 |
| BruteForce | SSH | 2018 | 93,818 | 93,818 |
| BruteForce | FTP | 2017 | 7,913 | 5,911 |
| BruteForce | SSH | 2017 | 2,977 | 2,977 |
| BruteForce | HTTP Form Login | 2017 | 151 | 151 |

## Cot da bo

- **Dinh danh / khong dung chung** (10): `Flow ID`, `Source IP`, `Source Port`, `Destination IP`, `Timestamp`, `Unnamed: 0`, `SimillarHTTP`, `Inbound`, `Protocol`, `Fwd Header Length.1`
- **Ro ri (thay bang dst_port_class)** (1): `Destination Port`
- **Hang so tuyet doi** (8): `Bwd PSH Flags`, `Bwd URG Flags`, `Fwd Avg Bytes/Bulk`, `Fwd Avg Packets/Bulk`, `Fwd Avg Bulk Rate`, `Bwd Avg Bytes/Bulk`, `Bwd Avg Packets/Bulk`, `Bwd Avg Bulk Rate`
- **Trung lap voi cot khac** (7): `Avg Fwd Segment Size`, `Avg Bwd Segment Size`, `Subflow Fwd Packets`, `Subflow Fwd Bytes`, `Subflow Bwd Packets`, `Subflow Bwd Bytes`, `CWE Flag Count`