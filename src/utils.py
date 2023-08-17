import os
import sys
import bz2
#import numpy as np
#import pandas as pd
import dill
import gzip
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from cachetools import LRUCache
from src.exception import CustomException
from functools import lru_cache
import logging
import io
#import chardet


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
def load_compressed_model_pickle(file):
    try:
        if file in cache:
            return cache[file]
        else:
            with bz2.BZ2File(file, 'rb') as f:
                compressed_model = f.read()
                compressed_model_io = io.BytesIO(compressed_model)
                loaded_model = pickle.load(compressed_model_io)
                cache[file] = loaded_model
                return loaded_model
    except Exception as e:
        raise CustomException(f"Error loading compressed model from file {file}: {e}", sys)



#def load_compressed_model(file):
#    try:
#        with bz2.BZ2File(file, 'rb') as f:
#            compressed_model = f.read()
#            loaded_model = pickle.load(compressed_model)
#            return loaded_model
#    except Exception as e:
#        print(f"Error loading compressed model: {e}")
#        return None


def load_compressed_gzip_model(file):
    with gzip.open(file, 'rb') as f:
        model = dill.load(f)
    return model


#def load_d_gz_model_to_check(path):
#    with gzip.open(path, 'rb') as f:
#        data = f.read()
#        encoding = chardet.detect(data)['encoding']
#        return data.decode(encoding)
#

def load_compressed_object(file):
    try:
        # Check that the file exists and is readable
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        if not os.access(file, os.R_OK):
            raise IOError(f"File is not readable: {file}")

        with bz2.BZ2File(file, 'rb') as file_object:
            data = bz2.BZ2File(file_object)
            data = pickle.load(data)
            return data
                                                         #Second compression approach
            #with open(file, 'rb') as file_object:
            #    decomp = bz2.BZ2Decompressor()
            #    data = file_object.read()
            #    decompressed_data = decomp.decompress(data)
            #    return pickle.loads(decompressed_data)

    except (FileNotFoundError, IOError) as e:
        # Handle file-related errors
        logging.error(f"Error loading compressed data from file {file}: {e}")
        raise CustomException(e, sys)

    except pickle.UnpicklingError as e:
        # Handle errors when unpickling data
        logging.error(f"Error unpickling data from file: {file}")
        raise CustomException(f"Error unpickling data from file: {file}", sys)

    except OSError as e:
        raise CustomException(f"Error loading compressed object from file {file}: {e}", sys)

    except Exception as e:
        # Handle other errors
        logging.error(f"An unexpected error occurred while loading compressed data from file {file}: {e}")
        raise CustomException(e, sys)


#l#oad_d_gz_model_to_check("artifacts/model.pkl.gz")

        #os.path.join('artifacts','model.pkl.gz')