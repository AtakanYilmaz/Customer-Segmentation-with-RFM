###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################

import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# 1 #
df_ = pd.read_excel("Hafta_03\Ödevler\online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()

df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]
df = df[~df["Invoice"].str.contains("C", na=False)]

# 2 #
df.head()
df.shape
df.describe().T

# 3 #

df.isnull().sum() # Descripton kolonun da 2928, Customer Id de 107927 adet eksik gözlem bulunmaktadır.

# 4 #

df.dropna(inplace=True)

# 5 #

df.nunique()

"""
Invoice        28816
StockCode       4632
Description     4681
Quantity         825
InvoiceDate    25296
Price           1606
Customer ID     4383
Country           40
"""
# 6 #

df["Description"].value_counts()
# df["Description"].value_counts().head()

# 7 #

df.groupby("Description").agg({"Quantity" : "sum"}).sort_values("Quantity", ascending=False).head(5)

# 8 #

#df = df[~df["Invoice"].str.contains("C", na=False)] üstte kod çalıştırıldı

# 9 #

df["TotalPrice"] = df["Quantity"] * df["Price"]


###############################################################
# RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

df["InvoiceDate"].max()

today_date = dt.datetime(2011,12,11)

rfm = df.groupby("Customer ID").agg({"InvoiceDate" : lambda date: (today_date - date.max()).days,
                                     "Invoice": lambda num: num.nunique(),
                                     "TotalPrice": lambda price: price.sum()})
rfm.head()

rfm.columns = ["Recency", "Frequency", "Monetary"]

rfm.head()

###############################################################
# RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

rfm["recency_score"] = pd.qcut(rfm["Recency"], 5, labels=[1,2,3,4,5])

rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[5,4,3,2,1])

rfm["monetary_score"] = pd.qcut(rfm["Monetary"], 5, labels=[5,4,3,2,1])

rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["frequency_score"].astype(str))

###############################################################
# RFM Segmentlerinin Oluşturulması
###############################################################

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segments"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)

rfm_loyal_customers = rfm[rfm["segments"] == "loyal_customers"]

rfm_loyal_customers.to_excel("Loyal_Customers.xlsx")

rfm[["segments", "Recency", "Frequency", "Monetary"]].groupby("segments").agg(["mean", "count"])

"""
 CustomerID  recency       T  frequency  monetary  expected_purc_1_week  expected_purc_1_month  expected_average_profit_clv        clv  scaled_clv segments
0       12747  52.2857 52.8571         11  381.4555                0.2025                 0.8077                     377.0011  1882.9582      0.0205        A
1       12748  53.1429 53.4286        209  154.9302                3.2375                12.9159                     154.8564 12377.8805      0.1349        A
2       12749  29.8571 30.5714          5  815.5880                0.1671                 0.6657                     793.2091  3238.1859      0.0353        A
3       12820  46.1429 46.7143          4  235.5850                0.1040                 0.4146                     228.9294   585.5092      0.0064        C
4       12822   2.2857 12.5714          2  474.4400                0.1291                 0.5127                     444.8168  1376.8501      0.0150        B
5       12823  31.5714 42.4286          5  351.9000                0.1221                 0.4869                     343.1242  1029.4704      0.0112        B
6       12826  51.7143 52.2857          7  210.6743                0.1418                 0.5657                     207.3372   724.9769      0.0079        C
7       12827   5.4286  6.4286          3  143.3833                0.2775                 1.0992                     139.0373   914.7514      0.0100        B
8       12828  18.1429 18.7143          6  169.7850                0.2650                 1.0539                     166.9100  1070.5596      0.0117        B
9       12829   3.2857 51.5714          2  143.6100                0.0043                 0.0171                     137.2276    14.4483      0.0002        D
"""

"""

"""
