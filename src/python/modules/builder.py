# Created by Samar on 19-05-2022
# Filename: builder.py

import pickle

import sklearn.metrics as mt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier


class models:
    def __init__(self):
        self.linear_estimators = [
            ('lda', LinearDiscriminantAnalysis()),
            ('svc', make_pipeline(StandardScaler(), LinearSVC(random_state=42))),
            ('knn', KNeighborsClassifier(n_neighbors=3))
        ]

        self.other_estimators = [
            ('dt', DecisionTreeClassifier(random_state=0)),
            ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
            ('nn', MLPClassifier(hidden_layer_sizes=(5, 2), random_state=0))
        ]

        self.inner_clf = StackingClassifier(
            estimators=self.other_estimators, final_estimator=LogisticRegression()
        )

        self.clf = StackingClassifier(
            estimators=self.linear_estimators, final_estimator=self.inner_clf
        )

        self.predicted_value = None
        self.accuracy = 0

    def fit(self, x, y):
        print("The stacking model has been fitted for train dataset")
        self.clf.fit(x, y)
        pickle.dump(models, open('../../models/stack_model.pkl', 'wb'))

    def pred(self, x_test):
        print("The stacking model successfully predicted test dataset", end="\n")
        # m = pickle.load(open('../../models/stack_model.pkl', 'rb'))
        self.predicted_value = self.clf.predict(x_test.values)
        return self.predicted_value

    def __metric(self, method, y_true, y_pred):
        if method == "accuracy":
            self.accuracy = mt.accuracy_score(y_true, y_pred) * 100
            print("Accuracy:", self.accuracy)
        elif method == "precision":
            print("Precision:", mt.precision_score(y_true, y_pred))
        elif method == "recall":
            print("Recall:", mt.recall_score(y_true, y_pred))
        elif method == "f1":
            print("F1 Score:", mt.f1_score(y_true, y_pred))
        elif method == "roc":
            print("ROC AUC (OVR):", mt.roc_auc_score(y_true, y_pred, multi_class="ovr"))
            print("ROC AUC (OVO):", mt.roc_auc_score(y_true, y_pred, multi_class="ovo"))

    def evaluate(self, y_true, y_pred, method=None):
        print("Evaluating the model performance")
        if method is None:
            self.accuracy = mt.accuracy_score(y_true, y_pred)*100
            print("Accuracy:", self.accuracy)
        else:
            if isinstance(method, str):
                self.__metric(str, y_true, y_pred)
            else:
                for i in method:
                    self.__metric(i, y_true, y_pred)
