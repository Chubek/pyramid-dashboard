from pyod.models.knn import KNN
from pyod.models.combination import aom, moa, average, maximization
from pyod.utils.utility import standardizer
import numpy as np
from dotenv import dotenv_values
import pandas as pd

temp = dotenv_values(".env")

def detect_anomaly(X_train, X_test, columns):
    X_train_norm, X_test_norm = standardizer(X_train, X_test)

    n_clf = 20
    k_list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 
        120, 130, 140, 150, 160, 170, 180, 190, 200]

    train_scores = np.zeros([X_train.shape[0], n_clf])
    test_scores = np.zeros([X_test.shape[0], n_clf])

    for i in range(n_clf):
        k = k_list[i]
        clf = KNN(n_neighbors=k, method='largest')
        clf.fit(X_train_norm)

        train_scores[:, i] = clf.decision_scores_
        test_scores[:, i] = clf.decision_function(X_test_norm)

    train_scores_norm, test_scores_norm = standardizer(train_scores, test_scores)

    if temp['METHOD_OD'] == "aom":
        y_by = aom(test_scores_norm, n_buckets=5)
    elif temp['METHOD_OD'] == "moa":
        y_by = moa(test_scores_norm, n_buckets=5)
    elif temp['METHOD_OD'] == "max":
        y_by = maximization(test_scores_norm)
    elif temp['METHOD_OD'] == "avg":
        y_by = average(test_scores_norm)


    df_test = pd.DataFrame()
    df_test[columns] = pd.DataFrame(X_test)
    df_test['y_by_score'] = y_by
    df_test['y_by_cluster'] = np.where(df_test['y_by_score']<0, 0, 1)

    return df_test