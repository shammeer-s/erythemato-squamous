# Created by Samar on 20-05-2022
# Filename: main.py

# Warning filters
import warnings

# Importing formatted data
from modules.base import declarations
from modules.builder import models
from modules.preprocess import data

warnings.simplefilter('ignore')

if __name__ == '__main__':
    print("\n#", "="*55, "#")
    # initializations
    base = declarations()
    raw_data = base.raw_data

    # preprocessing
    preprocess = data(raw_data)
    preprocess.imputer()

    if preprocess.correlated_features is None:
        preprocess.correlation()
    else:
        print(preprocess.correlated_features)
    preprocess.split()

    # model build
    model = models()
    model.fit(preprocess.x_train, preprocess.y_train)
    y_pred = model.pred(preprocess.x_test)
    model.evaluate(preprocess.y_test, y_pred)

    print("\n#", "=" * 55, "#\n")
