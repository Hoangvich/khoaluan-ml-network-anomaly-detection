# Buoc 6 - Giao thuc B: cross-dataset

Model: `HistGradientBoostingClassifier` (sample_weight balanced), cung cau hinh voi Buoc 5 de so sanh cong bang.

Metric chi tinh tren cac lop **co mat o ca train va test**. Cac lop khac van hien trong confusion matrix de thay chung bi day ve dau.

## Ket qua (Bang B)

| # | Train | Test | Dong train | Dong test | Lop danh gia | macro-F1 |
|---|---|---|---:|---:|---|---:|
| B1 | 2017 | 2018 | 2,290,303 | 591,454 | BENIGN, BruteForce | **0.4564** |
| B2 | 2017 | 2019 | 2,290,303 | 283,009 | BENIGN, DDoS | **0.0013** |
| B3 | 2018+2019 | 2017 | 874,463 | 2,290,303 | BENIGN, DDoS, BruteForce | **0.3723** |

### B1: train 2017 -> test 2018

```
              precision    recall  f1-score   support

      BENIGN     0.8411    0.9980    0.9128    497636
  BruteForce     0.0000    0.0000    0.0000     93818

   micro avg     0.8411    0.8397    0.8404    591454
   macro avg     0.4206    0.4990    0.4564    591454
weighted avg     0.7077    0.8397    0.7680    591454
```

Confusion matrix day du (hang = that, cot = du doan):

| that \ du doan | BENIGN | DDoS | PortScan | BruteForce |
|---|---|---|---|---|
| **BENIGN** | 496,623 | 28 | 984 | 1 |
| **DDoS** | 0 | 0 | 0 | 0 |
| **PortScan** | 0 | 0 | 0 | 0 |
| **BruteForce** | 93,818 | 0 | 0 | 0 |

### B2: train 2017 -> test 2019

```
              precision    recall  f1-score   support

      BENIGN     0.0013    1.0000    0.0025       359
        DDoS     0.0000    0.0000    0.0000    282650

   micro avg     0.0013    0.0013    0.0013    283009
   macro avg     0.0006    0.5000    0.0013    283009
weighted avg     0.0000    0.0013    0.0000    283009
```

Confusion matrix day du (hang = that, cot = du doan):

| that \ du doan | BENIGN | DDoS | PortScan | BruteForce |
|---|---|---|---|---|
| **BENIGN** | 359 | 0 | 0 | 0 |
| **DDoS** | 282,635 | 0 | 0 | 15 |
| **PortScan** | 0 | 0 | 0 | 0 |
| **BruteForce** | 0 | 0 | 0 | 0 |

### B3: train 2018+2019 -> test 2017

Lop chi co o test (khong the hoc duoc): `PortScan`

```
              precision    recall  f1-score   support

      BENIGN     0.9458    0.8683    0.9054   1992978
        DDoS     0.1414    0.3087    0.1940    128025
  BruteForce     0.0131    0.0271    0.0177     11047

    accuracy                         0.8303   2132050
   macro avg     0.3668    0.4013    0.3723   2132050
weighted avg     0.8926    0.8303    0.8581   2132050
```

Confusion matrix day du (hang = that, cot = du doan):

| that \ du doan | BENIGN | DDoS | PortScan | BruteForce |
|---|---|---|---|---|
| **BENIGN** | 1,730,487 | 239,963 | 0 | 22,528 |
| **DDoS** | 88,505 | 39,520 | 0 | 0 |
| **PortScan** _(khong co trong train)_ | 79,871 | 78,382 | 0 | 0 |
| **BruteForce** | 10,736 | 12 | 0 | 299 |

## Doi chieu Bang A vs Bang B

- Bang A (pooled, `RandomForest(100)`): macro-F1 = **0.9991**
- Bang B (cross-dataset, trung binh 3 thi nghiem): macro-F1 = **0.2767**
- **Chenh lech: +0.7224**

> Chenh lech nay chinh la phan hieu nang den tu viec ghi nho dac diem rieng cua tung testbed. Bang B moi phan anh kha nang phat hien tan cong tren mang chua tung thay.