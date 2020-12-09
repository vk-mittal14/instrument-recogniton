# -*- coding: utf-8 -*-
"""Music Classifier

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zwGfZP9nx2Q_is0dHIqUnbazRVu460Tq
"""

import pandas as  pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
import seaborn as sns
from sklearn.metrics import recall_score, precision_score, accuracy_score
from sklearn.metrics import confusion_matrix, f1_score, classification_report
import matplotlib.pyplot as plt

data = pd.read_csv('music_data_all.csv')
cl = ['tru', 'pia', 'flu', 'gac', 'org']
data = data.loc[data['class'].isin(cl)]

instruments = data.iloc[:, 2]
encoder = LabelEncoder()
y = encoder.fit_transform(instruments)

d= {}
for i, j in zip(list(set(y)), encoder.inverse_transform(list(set(y)))):
    d[i] = j

data.iloc[:, 3:21]

X = data.iloc[:, 3:21].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

svclassifier = SVC(kernel='rbf', C = 10.0, gamma=0.1)

svclassifier.fit(X_train, y_train)

predicted_labels = svclassifier.predict(X_test)

print("Recall: ", recall_score(y_test, predicted_labels,average=None))
print("Precision: ", precision_score(y_test, predicted_labels,average=None))
print("F1-Score: ", f1_score(y_test, predicted_labels, average=None))
print("Accuracy: %.2f  ," % accuracy_score(y_test, predicted_labels,normalize=True), accuracy_score(y_test, predicted_labels,normalize=False) )

print("Number of samples:",y_test.shape[0])
cnf = confusion_matrix(y_test, predicted_labels)
print(cnf)

df_cm = pd.DataFrame(cnf, index = [i for i in d.values()],
                  columns = [i for i in d.values()])

plt.figure(figsize = (10,7))
sns.heatmap(df_cm, annot=True)
plt.savefig('cnf.eps', format='eps')
