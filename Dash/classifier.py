import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
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

        print("---------------------------------------")

        print("Training Decision tree")
        tic = time()

        model = DecisionTreeClassifier(max_depth=50)
        model.fit(X_train, y_train)

        print(f"done in {time() - tic:.3f}s")
        print(f"Test R2 score: {model.score(X_test, y_test):.4f}")

        # print("Training random forest")
        # tic = time()
        #
        # clf = RandomForestClassifier(max_depth=5, random_state=0)
        # clf.fit(X_train, y_train)
        #
        # print(f"done in {time() - tic:.3f}s")
        # print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")
        #
        # print("Training QDA")
        # tic = time()
        #
        # clf = QuadraticDiscriminantAnalysis()
        # clf.fit(X_train, y_train)
        #
        # print(f"done in {time() - tic:.3f}s")
        # print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")
        #
        # print("Training LDA")
        # tic = time()
        #
        # clf = LinearDiscriminantAnalysis()
        # clf.fit(X_train, y_train)
        #
        # print(f"done in {time() - tic:.3f}s")
        # print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")
        #
        print("Training Kneighbor")
        tic = time()

        clf = KNeighborsClassifier(n_neighbors=3)
        clf.fit(X_train, y_train)

        vec=[[0.001398045, 0.003814933, 0.000297944, 0.003131537, 0.000225021, 0.005619264]]
        label=clf.predict(vec)

        print("Predicción kneighbor: "+str(label))

        print(f"done in {time() - tic:.3f}s")
        print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")
        #
        # print("Training NB")
        # tic = time()
        #
        # clf = GaussianNB()
        # clf.fit(X_train, y_train)
        #
        # print(f"done in {time() - tic:.3f}s")
        # print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")
        #
        # print("---------------------------------------")

        return model


    def predict_value(self,new_val):

        val=int(self.model.predict([new_val])[0])

        return val


def main():

    data='/Users/jpav/Documents/Enose/Dash/Data_processed/Models/classifier_v1.csv'
    classifier=odor_classifier(data)
    vec=[1.399665643,0.480775266,1.068716594,0.14040973,0.204368711,0.68769421]
    label=classifier.predict_value(vec)
    print("predicted:" + str(label))

    return 0


if __name__ == "__main__":
    main()
