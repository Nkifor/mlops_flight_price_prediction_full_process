import os
import sys

import numpy as np
import pandas as pd
import dill
import pickle

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