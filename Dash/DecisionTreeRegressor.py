import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from time import time
from sklearn.tree import DecisionTreeRegressor

#   SB-51-00       ----- 0
#   SP-11-00       ----- 1
#   SP-19-01       ----- 2
#   TGS2602        ----- 3
#   TGS2620        ----- 4
#   SP-31-00       ----- 5
#   SP3S-AQ2-01    ----- 6

class regressionModels:

    def __init__(self, model_data):

        self.model_SB5100 = self.createModel(model_data,"SB-51-00")
        self.model_SP1100 = self.createModel(model_data,"SP-11-00")
        self.model_SP1901 = self.createModel(model_data,"SP-19-01")
        self.model_TGS2602 = self.createModel(model_data,"TGS2602-B00")
        self.model_TGS2620 = self.createModel(model_data,"TGS2620-C00")
        self.model_SP3100 = self.createModel(model_data,"SP-31-00")
        self.model_SP3SAQ201 = self.createModel(model_data,"SP3S-AQ2-01")

        self.dictModels = {"SB-51-00": self.model_SB5100, "SP-11-00": self.model_SP1100,"SP-19-01": self.model_SP1901,
                    "TGS2602-B00": self.model_TGS2602, "TGS2620-C00": self.model_TGS2620,
                    "SP-31-00": self.model_SP3100,  "SP3S-AQ2-01": self.model_SP3SAQ201}

    def createModel(self, data, sensor):

        X = pd.DataFrame()

        X=data[["In_Temperature","In_Humidity"]]
        y = data[[sensor]].values.ravel()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        print("Training DecisionTreeRegressor... for: "+sensor)
        tic = time()
        model = DecisionTreeRegressor(max_depth=20)
        model.fit(X_train, y_train)

        print(f"done in {time() - tic:.3f}s")
        print(f"Test R2 score: {model.score(X_test, y_test):.4f}")

        return model

    def predict_value(self, temp, hum, sensor):

        val=self.dictModels.get(sensor).predict([[temp,hum]])[0]
        return val

def main():

    data=pd.read_csv('./Data_processed/Models/reg_data.csv')
    models = regressionModels(data)
    val= models.predict_value(30,55,"SP-11-00")
    print("Predict "+str(val))

    return 0


if __name__ == "__main__":
    main()
