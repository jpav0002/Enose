import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from time import time
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor

X = pd.DataFrame()
Sensor = pd.read_csv('/Users/jpav/Documents/Enose/WekaData_Enose/TGS2602.csv')

X=Sensor[["In_Temperature","In_Humidity","Out_Temperature","Out_Humidity"]]
y = Sensor.iloc[:,-1:]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

print("Training MLPRegressor...")
tic = time()
est = MLPRegressor(hidden_layer_sizes=(50,10), activation='relu', solver='lbfgs',
                         max_iter=2000, learning_rate='constant', learning_rate_init=0.001,
                         random_state=42)
est.fit(X_train, y_train.values.ravel())

print(f"done in {time() - tic:.3f}s")
print(f"Test R2 score: {est.score(X_test, y_test.values.ravel()):.4f}")

print(f"Prediccion:  {est.predict([[32.35818011,27.0748455,32.89534505,25.68309028]])}")

print("Training DecisionTreeRegressor...")
tic = time()
regr_2 = DecisionTreeRegressor(max_depth=5)
regr_2.fit(X, y)

print(f"done in {time() - tic:.3f}s")
print(f"Test R2 score: {regr_2.score(X_test, y_test.values.ravel()):.4f}")

print(f"Prediccion DecisionTreeRegressor:  {regr_2.predict([[32.35818011,27.0748455,32.89534505,25.68309028]])}")
