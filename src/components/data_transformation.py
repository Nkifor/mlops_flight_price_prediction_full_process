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
from scipy.sparse import hstack


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
                #"Unnamed: 0",
                "duration",
                "days_left",
                #"price",
            ]
            categorical_columns=[
                "airline",
                #"flight",
                "source_city",
                "departure_time",
                "stops",
                "arrival_time",
                "destination_city",
                "class",
            ]

            numerical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )



            categorical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info(f"Numerical columns: {numerical_columns} imputation and standard scaling completed.")
            logging.info(f"Categorial columns: {categorical_columns} imputation encoding completed and standard scaling completed.")

            preprocessor=ColumnTransformer(
                [
                    ("numerical_pipeline",numerical_pipeline,numerical_columns),
                    ("categorical_pipeline",categorical_pipeline,categorical_columns)
                ]

            )

            return preprocessor


        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            f"{print(train_df)} /\ tu powinien byc df z trainem"
            f"{print(test_df)} /\ tu powinien byc df z testem"


            logging.info(f"Read test and train data as dataframe completed. {print(train_df.columns)}  {print(test_df.columns)}")
            logging.info("Obtaining preprocessor object.")

            preprocessing_object=self.get_data_transformer_object()

            target_column_name="price"
            columns_to_drop=[
                "Unnamed: 0",
                "flight",
                "price"]
            target_feature_train_df=train_df[target_column_name]
            input_feature_train_df=train_df.drop(columns=columns_to_drop,axis=1)

            target_feature_test_df=test_df[target_column_name]
            input_feature_test_df=test_df.drop(columns=columns_to_drop,axis=1)


            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe. ")
            #print(input_feature_train_df)
            #print(input_feature_test_df)

            input_feature_train_arr=preprocessing_object.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_object.transform(input_feature_test_df)

            print(input_feature_train_arr)
            print(target_feature_train_df)

            print(input_feature_train_arr.shape)
            print(target_feature_train_df.shape)

            #print(input_feature_test_arr.shape[0])
            #print(target_feature_test_df.shape[0])

            #print(input_feature_train_arr)
            #print(input_feature_test_arr)
            #print(target_feature_train_df)
            #print(target_feature_test_df)

            target_feature_train_arr = np.array(target_feature_train_df).reshape(-1, 1)
            target_feature_test_arr = np.array(target_feature_test_df).reshape(-1, 1)

            print(input_feature_train_arr)
            print(target_feature_train_arr)

            print(input_feature_train_arr.shape)
            print(target_feature_train_arr.shape)

            train_arr = hstack([input_feature_train_arr, target_feature_train_arr])

            #np.array
            test_arr = hstack([input_feature_test_arr, target_feature_test_arr])

            logging.info(f'Saved preprocessing object.')

            save_object(

                file=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_object


            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
