import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import joblib

df = pd.read_csv("csv/dataset.csv")
df.head()

df = df.drop(df.columns[[6]], axis=1)
df = df.replace(np.nan, 0.0)
df.head()

x = df.drop(df.columns[[0]], axis=1)
x = df.drop(df.columns[[0]], axis=1)
x.head()

x.isnull().sum()
y = df[df.columns[[0]]]
y.head()
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2, random_state=42)
yTrain = np.asarray(yTrain).reshape(-1, 1)

model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(xTrain, yTrain)
joblib.dump(model, "MalariaClassifier")

print(yTest,xTest)
predictions = model.predict([[15047.5,0.0,0.0,0.0,0.0]])
print(predictions)
#print(metrics.classification_report(predictions, yTest))
#print(model.score(xTest, yTest))