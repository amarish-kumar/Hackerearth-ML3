'''
Building a Model using XGBoost
'''

import sys
import datetime
import numpy as np
import pandas as pd
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import train_test_split

# --------------------- Initializing variables

start_time = datetime.datetime.now()
print("Started at: " + str(start_time))
pred_df = pd.DataFrame()

# --------------------- Loading datasets

train = pd.read_csv("Data\\train_pp1.csv", header=0)
test = pd.read_csv("Data\\test_pp1.csv", header=0)


# --------------------- Imputing siteid

train['siteid'].fillna(-999, inplace=True)
test['siteid'].fillna(-999, inplace=True)

train['hour_range'] = np.where(train['hour'].isin([0,1,20,21,22,23]), 1, 0)
test['hour_range'] = np.where(test['hour'].isin([0,1,20,21,22,23]), 1, 0)

# --------------------- Dropping columns

pred_df['ID'] = test['ID']
cols_to_drop = ['ID', 'datetime', 'weekday','minute','siteid']
train.drop(cols_to_drop, axis=1, inplace=True)
test.drop(cols_to_drop, axis=1, inplace=True)

# --------------------- Splitting data

Y = train['click']
train.drop('click', axis=1, inplace=True)
X = train
# test = test.as_matrix()
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=125)
# X_train = X_train.as_matrix()
# X_test = X_test.as_matrix()
# y_train = y_train.as_matrix()
# y_test = y_test.as_matrix()

# --------------------- Creating model

xgbclassifier = XGBClassifier(n_estimators=100, nthread=-1, silent=False, seed=125, learning_rate=0.2)
# xgbmodel = xgbclassifier.fit(X_train, y_train)
xgbmodel = xgbclassifier.fit(X, Y)

# pred = xgbmodel.predict(test)
xgbmodel.score(X_test, y_test)
pred = xgbmodel.predict_proba(test)[:,1]


# --------------------- Writing results

pred_df['click'] = pred
file_name = "Predictions\\prediction_" + str(datetime.datetime.now().date()) + "_" +\
            str(datetime.datetime.now().strftime("%H%M%S")) + ".csv"
pred_df.to_csv(path_or_buf="Predictions\\prediction_9.csv", index=False)