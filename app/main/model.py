import os
import pandas as pd
import pickle

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split

from scipy.stats import randint
from xgboost import XGBClassifier

train = pd.read_csv('/Users/giyun/Prj3/data/flask_train.csv')
target = pd.read_csv('/Users/giyun/Prj3/data/flask_target.csv')

X = train
y = target

X = X.drop(['Unnamed: 0'], axis=1)
y = y.drop(['Unnamed: 0'], axis=1)

classifier = XGBClassifier()

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8)

classifier.fit(X_train, y_train)

with open('model.pkl','wb') as pickle_file:
    pickle.dump(classifier, pickle_file)
