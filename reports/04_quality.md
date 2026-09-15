# Buoc 4 - Bao cao kiem dinh chat luong

- Tong dong: **3,305,401**
- Cot dau vao: **62**
- Group phan biet: **2,623,782**

## 1. Tinh sach

| Kiem tra | Ket qua | Dat |
|---|---:|---|
| Gia tri NaN | 0 | PASS |
| Gia tri Inf | 0 | PASS |
| Flow Duration < 0 | 0 | PASS |
| Flow 0 byte | 0 | PASS |
| Gia tri bat kha thi ve vat ly | 0 | PASS |

> Gia tri bat kha thi = do dai header / kich thuoc segment / IAT am (ngoai sentinel `-1`). Do la loi tran so cua CICFlowMeter, tap trung o DDoS-2019 nen tuong quan voi nhan -> da loc bo o buoc 3.

## 2. Cot hang so / gan hang so (tinh lai tren dataset cuoi)

| Cot | So gia tri | Gia tri pho bien | Ti le |
|---|---:|---:|---:|
| `Fwd URG Flags` | 2 | 0 | 100.000% |

> Cac cot nay gan nhu khong mang thong tin. Giu lai vi mot so (vd. co RST/FIN) van huu ich cho lop hiem; can theo doi o feature importance.

## 3. Tuong quan Spearman |rho| > 0.98 (mau 300,000 dong)

| Feature A | Feature B | \|rho\| |
|---|---|---:|
| `Packet Length Std` | `Packet Length Variance` | 1.0000 |
| `Fwd PSH Flags` | `SYN Flag Count` | 0.9997 |
| `Idle Max` | `Idle Mean` | 0.9996 |
| `Active Max` | `Active Mean` | 0.9994 |
| `Idle Mean` | `Idle Min` | 0.9993 |
| `ECE Flag Count` | `RST Flag Count` | 0.9989 |
| `Idle Max` | `Idle Min` | 0.9983 |
| `Active Mean` | `Active Min` | 0.9982 |
| `Flow IAT Mean` | `Flow Packets/s` | 0.9978 |
| `Bwd IAT Max` | `Bwd IAT Total` | 0.9977 |
| `Flow Packets/s` | `Fwd Packets/s` | 0.9976 |
| `Bwd IAT Max` | `Bwd IAT Mean` | 0.9974 |
| `Active Max` | `Active Min` | 0.9966 |
| `Fwd IAT Max` | `Fwd IAT Mean` | 0.9963 |
| `Bwd IAT Mean` | `Bwd IAT Total` | 0.9957 |
| `Fwd IAT Max` | `Fwd IAT Total` | 0.9953 |
| `Flow IAT Mean` | `Fwd Packets/s` | 0.9951 |
| `Average Packet Size` | `Packet Length Mean` | 0.9925 |
| `Fwd IAT Mean` | `Fwd IAT Total` | 0.9921 |
| `Flow Duration` | `Flow IAT Max` | 0.9914 |
| `Fwd Packet Length Min` | `Min Packet Length` | 0.9903 |
| `Flow IAT Max` | `Flow Packets/s` | 0.9864 |
| `Flow IAT Max` | `Fwd Packets/s` | 0.9863 |
| `Bwd Packet Length Max` | `Total Length of Bwd Packets` | 0.9806 |

> Chi bao cao, KHONG tu dong bo: model cay khong bi anh huong boi da cong tuyen, nhung feature importance se bi chia se giua cac cot nay.

## 4. Kiem tra ro ri - AUC don bien one-vs-rest

Mot feature don le tach duoc mot lop voi AUC > 0.99 la dau hieu **fingerprint testbed** chu khong phai hanh vi tan cong.

| Lop | Feature | AUC |
|---|---|---:|
| BENIGN | `Bwd Packet Length Min` | 0.7344 |
| BENIGN | `Packet Length Mean` | 0.6598 |
| BENIGN | `Average Packet Size` | 0.6525 |
| DoS/DDoS | `Average Packet Size` | 0.8516 |
| DoS/DDoS | `Bwd Packets/s` | 0.8506 |
| DoS/DDoS | `Packet Length Mean` | 0.8483 |
| PortScan | `Total Length of Fwd Packets` | 0.9959 **<- nghi ngo** |
| PortScan | `Fwd Packet Length Max` | 0.9904 **<- nghi ngo** |
| PortScan | `Fwd Packet Length Mean` | 0.9902 **<- nghi ngo** |
| BruteForce | `Fwd Header Length` | 0.9486 |
| BruteForce | `Bwd Header Length` | 0.9411 |
| BruteForce | `Total Fwd Packets` | 0.9376 |

- Feature nghi ngo ro ri: `Total Length of Fwd Packets` (PortScan, AUC=0.996), `Fwd Packet Length Max` (PortScan, AUC=0.990), `Fwd Packet Length Mean` (PortScan, AUC=0.990)

## 5. Trung lap theo lop x nguon

| Lop | Nguon | Dong | Group phan biet | Trung lap |
|---|---|---:|---:|---:|
| BENIGN | 2017 | 1,990,409 | 1,685,227 | 15.3% |
| BENIGN | 2018 | 497,636 | 441,556 | 11.3% |
| BENIGN | 2019 | 355 | 353 | 0.6% |
| DoS/DDoS | 2017 | 307,534 | 306,537 | 0.3% |
| DoS/DDoS | 2019 | 246,355 | 85,586 | 65.3% |
| PortScan | 2017 | 158,253 | 1,963 | 98.8% |
| BruteForce | 2017 | 11,041 | 9,039 | 18.1% |
| BruteForce | 2018 | 93,818 | 93,818 | 0.0% |

> PortScan trung lap ~99% vi sau khi bo `Destination Port` moi flow quet port tro nen giong het nhau. Vi vay **bat buoc** dung GroupShuffleSplit theo `group_id` o buoc 5, neu khong metric se bi thoi phong nghiem trong.