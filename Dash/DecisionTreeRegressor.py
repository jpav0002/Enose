import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from time import time
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import QuantileTransformer
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor

def create_model(data, sensor):

    X = pd.DataFrame()
    #Sensor = pd.read_csv('/Users/jpav/Documents/Enose/smartiago_v2/Mean_Data.csv')
    #Sensor = pd.read_csv('D:\\repo\\Enose\\smartiago_v2\\Mean_Data.csv')

    X=data[["In_Temperature","In_Humidity"]]
    y = data[[sensor]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    print("Training DecisionTreeRegressor... for: "+sensor)
    tic = time()
    model = DecisionTreeRegressor(max_depth=10)
    model.fit(X, y)

    print(f"done in {time() - tic:.3f}s")
    print(f"Test R2 score: {model.score(X_test, y_test.values.ravel()):.4f}")

    return model

def main():

    print("Decision tree")

    return 0


if __name__ == "__main__":
    main()
