import warnings

import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from data_indexer import data

warnings.simplefilter('ignore')

correlation = pd.read_csv("../input/output.csv", index_col=0)
correlation = correlation.loc[(correlation["Correlation"] >= 0.1) | (correlation["Correlation"] <= -0.1), :]

cols = correlation.index

data = data.loc[:, cols | ['disease']]

x = data.loc[:, cols].values
y = data.loc[:, 'disease'].values

low = 93.47
high = 93.47
tot = 0
n = 100
for i in range(n):
    print("Random State:", i)
    x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, random_state=i, test_size=0.25)

    linear_estimators = [
        ('lda', LinearDiscriminantAnalysis()),
        ('svc', make_pipeline(StandardScaler(), LinearSVC(random_state=42))),
        ('knn', KNeighborsClassifier(n_neighbors=3))
    ]

    other_estimators = [
        ('dt', DecisionTreeClassifier(random_state=0)),
        ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
        ('nn', MLPClassifier(hidden_layer_sizes=(5, 2), random_state=0))
    ]

    inner_clf = StackingClassifier(
        estimators=other_estimators, final_estimator=LogisticRegression()
    )

    clf = StackingClassifier(
        estimators=linear_estimators, final_estimator=inner_clf
    )
    score = clf.fit(x_train, y_train).score(x_test, y_test)*100
    tot += score

    if score < low:
        low = score
    elif score > high:
        high = score
    # sns.displot(data, x="disease", kind="kde")
    # sns.displot(y_test, kind="kde")
    # plt.show()

    # y_pred = clf.predict(x_test)
    # cm = confusion_matrix(y_test, y_pred)
    # sns.heatmap(cm, annot=True)
    # plt.show()

print("Low Accuracy:", low)
print("High Accuracy:", high)
print("Average Accuracy:", tot/n)
