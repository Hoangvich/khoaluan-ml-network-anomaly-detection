# Buoc 1 - Kiem dinh schema va nhan

## 1. Schema tho

- **2017**: 8 file, 79 cot -> `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
- **2018**: 1 file, 80 cot -> `02-14-2018.csv`
- **2019**: 1 file, 88 cot -> `Random_combine_final.csv`

## 2. Ket qua hop nhat

- Cot duy nhat sau chuan hoa: 2017=79, 2018=80, 2019=88
- **Giao cua 3 bo: 78 cot**
- 2018 khong khop 2017: `['Protocol', 'Timestamp']`
- 2017 khong khop 2018: `['Fwd Header Length.1']`
- 2019 thua so voi 2017: `['Destination IP', 'Flow ID', 'Inbound', 'Protocol', 'SimillarHTTP', 'Source IP', 'Source Port', 'Timestamp', 'Unnamed: 0']`

> Assert PASS: dung 78 cot chung; 2018 chi thua `Protocol`, `Timestamp`;
> 2017 chi thua `Fwd Header Length.1` (ban trung lap, se bo).

## 3. Feature dung de train: 61 so + 1 dan xuat = **62**

<details><summary>Danh sach feature</summary>

  1. `ACK Flag Count`
  2. `Active Max`
  3. `Active Mean`
  4. `Active Min`
  5. `Active Std`
  6. `Average Packet Size`
  7. `Bwd Header Length`
  8. `Bwd IAT Max`
  9. `Bwd IAT Mean`
 10. `Bwd IAT Min`
 11. `Bwd IAT Std`
 12. `Bwd IAT Total`
 13. `Bwd Packet Length Max`
 14. `Bwd Packet Length Mean`
 15. `Bwd Packet Length Min`
 16. `Bwd Packet Length Std`
 17. `Bwd Packets/s`
 18. `Down/Up Ratio`
 19. `ECE Flag Count`
 20. `FIN Flag Count`
 21. `Flow Bytes/s`
 22. `Flow Duration`
 23. `Flow IAT Max`
 24. `Flow IAT Mean`
 25. `Flow IAT Min`
 26. `Flow IAT Std`
 27. `Flow Packets/s`
 28. `Fwd Header Length`
 29. `Fwd IAT Max`
 30. `Fwd IAT Mean`
 31. `Fwd IAT Min`
 32. `Fwd IAT Std`
 33. `Fwd IAT Total`
 34. `Fwd PSH Flags`
 35. `Fwd Packet Length Max`
 36. `Fwd Packet Length Mean`
 37. `Fwd Packet Length Min`
 38. `Fwd Packet Length Std`
 39. `Fwd Packets/s`
 40. `Fwd URG Flags`
 41. `Idle Max`
 42. `Idle Mean`
 43. `Idle Min`
 44. `Idle Std`
 45. `Init_Win_bytes_backward`
 46. `Init_Win_bytes_forward`
 47. `Max Packet Length`
 48. `Min Packet Length`
 49. `PSH Flag Count`
 50. `Packet Length Mean`
 51. `Packet Length Std`
 52. `Packet Length Variance`
 53. `RST Flag Count`
 54. `SYN Flag Count`
 55. `Total Backward Packets`
 56. `Total Fwd Packets`
 57. `Total Length of Bwd Packets`
 58. `Total Length of Fwd Packets`
 59. `URG Flag Count`
 60. `act_data_pkt_fwd`
 61. `min_seg_size_forward`

</details>

## 4. Nhan tho -> lop muc tieu

| Nguon | File | Nhan tho | So dong | -> Lop |
|---|---|---|---:|---|
| 2017 | Friday-WorkingHours-Afternoon-DDos | `DDoS` | 128,027 | DoS/DDoS |
| 2017 | Friday-WorkingHours-Afternoon-DDos | `BENIGN` | 97,718 | BENIGN |
| 2017 | Friday-WorkingHours-Afternoon-Port | `PortScan` | 158,930 | PortScan |
| 2017 | Friday-WorkingHours-Afternoon-Port | `BENIGN` | 127,537 | BENIGN |
| 2017 | Friday-WorkingHours-Morning.pcap_I | `BENIGN` | 189,067 | BENIGN |
| 2017 | Friday-WorkingHours-Morning.pcap_I | `Bot` | 1,966 | _(loai bo)_ |
| 2017 | Monday-WorkingHours.pcap_ISCX.csv | `BENIGN` | 529,918 | BENIGN |
| 2017 | Thursday-WorkingHours-Afternoon-In | `BENIGN` | 288,566 | BENIGN |
| 2017 | Thursday-WorkingHours-Afternoon-In | `Infiltration` | 36 | _(loai bo)_ |
| 2017 | Thursday-WorkingHours-Morning-WebA | `BENIGN` | 168,186 | BENIGN |
| 2017 | Thursday-WorkingHours-Morning-WebA | `Web Attack ? Brute Force` | 1,507 | BruteForce |
| 2017 | Thursday-WorkingHours-Morning-WebA | `Web Attack ? XSS` | 652 | _(loai bo)_ |
| 2017 | Thursday-WorkingHours-Morning-WebA | `Web Attack ? Sql Injection` | 21 | _(loai bo)_ |
| 2017 | Tuesday-WorkingHours.pcap_ISCX.csv | `BENIGN` | 432,074 | BENIGN |
| 2017 | Tuesday-WorkingHours.pcap_ISCX.csv | `FTP-Patator` | 7,938 | BruteForce |
| 2017 | Tuesday-WorkingHours.pcap_ISCX.csv | `SSH-Patator` | 5,897 | BruteForce |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `BENIGN` | 440,031 | BENIGN |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `DoS Hulk` | 231,073 | DoS/DDoS |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `DoS GoldenEye` | 10,293 | DoS/DDoS |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `DoS slowloris` | 5,796 | DoS/DDoS |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `DoS Slowhttptest` | 5,499 | DoS/DDoS |
| 2017 | Wednesday-workingHours.pcap_ISCX.c | `Heartbleed` | 11 | _(loai bo)_ |
| 2018 | 02-14-2018.csv | `Benign` | 667,626 | BENIGN |
| 2018 | 02-14-2018.csv | `FTP-BruteForce` | 193,360 | BruteForce |
| 2018 | 02-14-2018.csv | `SSH-Bruteforce` | 187,589 | BruteForce |
| 2019 | Random_combine_final.csv | `TFTP` | 85,512 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `Syn` | 27,668 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `MSSQL` | 24,652 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_SNMP` | 21,856 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_DNS` | 21,686 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_MSSQL` | 19,308 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_NetBIOS` | 17,588 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `UDP` | 16,447 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `NetBIOS` | 15,563 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_UDP` | 13,237 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_SSDP` | 11,184 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_LDAP` | 9,090 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `LDAP` | 8,228 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `DrDoS_NTP` | 5,131 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `UDP-lag` | 1,547 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `Portmap` | 805 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `BENIGN` | 487 | BENIGN |
| 2019 | Random_combine_final.csv | `UDPLag` | 8 | DoS/DDoS |
| 2019 | Random_combine_final.csv | `WebDDoS` | 3 | DoS/DDoS |

## 5. Tong hop theo nguon x lop

| Nguon | BENIGN | DoS/DDoS | PortScan | BruteForce | (loai bo) |
|---|---|---|---|---|---|
| 2017 | 2,273,097 | 380,688 | 158,930 | 15,342 | 2,686 |
| 2018 | 667,626 | - | - | 380,949 | - |
| 2019 | 487 | 299,513 | - | - | - |
| **Tong** | **2,941,210** | **680,201** | **158,930** | **396,291** | **2,686** |