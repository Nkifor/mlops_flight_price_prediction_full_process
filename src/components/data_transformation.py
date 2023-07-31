import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This method will return the preprocessor
        object which will be used for data transformation.
        """
        try:
            numerical_columns=[
                'Unnamed: 0',
                'duration',
                'days_left',
                'price']
            categorical_columns=[
                'airline',
                'flight',
                'source_city',
                'departure_time',
                'stops',
                'arrival_time',
                'destination_city',
                'class',]

            numerical_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )

            logging.info("Numerical columns imputation and standard scaling completed.")

            categorical_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('onehot',OneHotEncoder()),
                    ('scaler',StandardScaler())
                ]
            )

            logging.info("Categorial columns imputation encoding completed and standard scaling completed.")

            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipeline",numerical_pipeline,numerical_columns),
                    ("categorical_pipeline",categorical_pipeline,categorical_columns)
                ]

            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_data_path,test_data_path):

        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)

            logging.info("Read test and train data as dataframe completed.")
            logging.info("Obtaining preprocessor object.")

            preprocessor_object=self.get_data_transformer_object()

            target_column_name='price'
            numerical_columns=[
                'Unnamed: 0',
                'duration',
                'days_left',
                'price']

            input_features_train_df=train_df.drop(target_column_name,axis=1)

        except:
