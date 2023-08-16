import os
import sys
import bz2
import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def save_object(file, obj):
    """
    This method will save the object in the file path provided.
    """
    try:
        dir_path = os.path.dirname(file)
        os.makedirs(dir_path, exist_ok=True)

        with open(file, 'wb') as file_object:
            dill.dump(obj, file_object)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train,X_test,y_test,models
                    ,param
                    ):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file):
    try:
        with open(file, 'rb') as file_object:

            return pickle.load(file_object)

    except Exception as e:
        raise CustomException(e, sys)


def load_compressed_object(file):
    try:                                                     #First  compression approach
        with bz2.BZ2File(file, 'rb') as file_object:
            return pickle.load(file_object)
    except Exception as e:
        raise CustomException(e, sys)
    #try:                                                      #Second compression approach
    #    with open(file, 'rb') as file_object:
    #        decomp = bz2.BZ2Decompressor()
    #        data = file_object.read()
    #        decompressed_data = decomp.decompress(data)
    #        return pickle.loads(decompressed_data)


    except Exception as e:
        raise CustomException(e, sys)