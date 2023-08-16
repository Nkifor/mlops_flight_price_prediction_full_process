import os
import sys
import bz2
import numpy as np
import pandas as pd
import dill
from pickle import load
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from cachetools import LRUCache
import concurrent.futures
from src.exception import CustomException
from functools import lru_cache


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

            return load(file_object)

    except Exception as e:
        raise CustomException(e, sys)






class LRUCache(dict):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        super().__init__()

    def __setitem__(self, key, value):
        if len(self) >= self.maxsize:
            oldest = next(iter(self))
            del self[oldest]
        super().__setitem__(key, value)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.pop(key)
        self[key] = value
        return value

cache = LRUCache(maxsize=100)

@lru_cache(maxsize=100)
def load_compressed_object_joblib(file):
    try:
        if file in cache:
            return cache[file]
        else:
            with bz2.BZ2File(file, 'rb') as f:
                obj = load(f)
                cache[file] = obj
                return obj
    except EOFError as e:
        raise CustomException(f"Error loading compressed object from file {file}: {e}. The compressed data may be incomplete or corrupted. Please regenerate the file or obtain a new copy.", sys)
    except Exception as e:
        raise CustomException(f"Error loading compressed object from file {file}: {e}", sys)




#def load_compressed_object(file):
#    try:                                                     #First  compression approach
#        with bz2.BZ2File(file, 'rb') as file_object:
#            return pickle.load(file_object)
#    #except Exception as e:
#    #    raise CustomException(e, sys)
#    #try:                                                      #Second compression approach
#    #    with open(file, 'rb') as file_object:
#    #        decomp = bz2.BZ2Decompressor()
#    #        data = file_object.read()
#    #        decompressed_data = decomp.decompress(data)
#    #        return pickle.loads(decompressed_data)
#
#
#    except Exception as e:
#        raise CustomException(e, sys)