# detect_outliers.py
import numpy as np

def detect_outliers(data):
    Q1 = np.percentile(data, 0)
    Q3 = np.percentile(data, 100)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = (data < lower_bound) | (data > upper_bound)

    return data[outliers], data[~outliers]  # Возвращаем и выбросы, и данные без выбросов

if __name__ == "__main__":
    data = np.array([41.78113947048308, 38.110507124468946, 26.036568174467888, 43.72893930997113, 14.105145869731038, 54.35327957088433])
    detected_outliers, data_without_outliers = detect_outliers(data)

    mean_with_outliers = np.mean(data)
    mean_without_outliers = np.mean(data_without_outliers)

    print("Original Data:", data)
    print("Detected Outliers:", detected_outliers)
    print("Mean (with outliers):", mean_with_outliers)
    print("Mean (without outliers):", mean_without_outliers)


# _id
# 656e02524ac6cc6ec0528844
# eas_event_id
# "2018-12-18_ev_01:32:10.273.730.507"
# decor_event_id
# "2018-12-18_ne_01:32:10.273.730.831"
# decor_Theta
# 41.14
# decor_Phi
# 208.2
#
# eas_events_corners
# Array (6)
#
# 0
# Object
# cluster
# 1
# theta
# 41.78113947048308
# phi
# 197.42570729245006
#
# 1
# Object
# cluster
# 3
# theta
# 38.110507124468946
# phi
# 207.07600826015658
#
# 2
# Object
# cluster
# 5
# theta
# 26.036568174467888
# phi
# 208.30620362746288
#
# 3
# Object
# cluster
# 6
# theta
# 43.72893930997113
# phi
# 217.5125079619563
#
# 4
# Object
# cluster
# 7
# theta
# 14.105145869731038
# phi
# 54.0699705436785
#
# 5
# Object
# cluster
# 8
# theta
# 54.35327957088433
# phi
# 217.21049231267634
