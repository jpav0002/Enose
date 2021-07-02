import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from time import time

class odor_classifier:

    def __init__ (self, csv_file):

        data_clf=pd.read_csv(csv_file)

        self.model = self.createModel(data_clf)


    def createModel(self,data):

        X=[]

        for col in data.columns:

            if (('Date' not in col) and ('Time' not in col) and ('Intensity' not in col)

                        and ('Humidity' not in col) and ('Temperature' not in col) and ("TGS2602" not in col)):

                X.append(col)

        X=data[X]
        y=data[['Intensity']].values.ravel()

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        print("Training tree")
        tic = time()

        clf = DecisionTreeRegressor(max_depth=20)
        clf.fit(X_train, y_train)

        print(f"done in {time() - tic:.3f}s")
        print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")

        return clf


    def predict_value(self,new_val):

        val=int(round(self.model.predict([new_val])[0],0))
        print('Predict: '+str(val))

        return val


def main():

    data='/Users/jpav/Documents/Enose/Dash/Data_processed/Models/classifier_v1.csv'
    classifier=odor_classifier(data)
    vec=[0,0,0,0,0,0]
    classifier.predict_value(vec)

    return 0


if __name__ == "__main__":
    main()
