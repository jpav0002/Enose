import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from time import time

def createModel(data):

    X=[]

    for col in data.columns:

        if (('Date' not in col) and ('Time' not in col) and ('Average' not in col) and ('Humidity' not in col) and ('Temperature' not in col)):
            X.append(col)

    X=data[X]
    y=data[['Average']].values.ravel()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    print("Training QDA")
    tic = time()

    clf = QuadraticDiscriminantAnalysis()
    clf.fit(X, y)

    print(f"done in {time() - tic:.3f}s")
    print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")

    print("Training tree")
    tic = time()

    clf = tree.DecisionTreeClassifier()
    clf.fit(X, y)

    print(f"done in {time() - tic:.3f}s")
    print(f"Test R2 score: {clf.score(X_test, y_test):.4f}")

def predic_value(new_val):

    


def main():

    data=pd.read_csv('./Data_processed/processed_classifier.csv')
    createModel(data)

    return 0


if __name__ == "__main__":
    main()
