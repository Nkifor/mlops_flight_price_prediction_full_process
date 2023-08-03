import sys
import os
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path =os.path.join('artifacts', 'model.pkl')
            preprocessor_path = os.path.join('artifacts','proprocessor.pkl')
            print("Before Loading")
            model=load_object(file=model_path)
            preprocessor=load_object(file=preprocessor_path)
            print("After Loading")
            data_scaled=preprocessor.transform(features)
            model_prediction=model.predict(data_scaled)
            return model_prediction
        except Exception as e:
            raise CustomException(e,sys)





class CustomData:
    def __init__(self,
        duration: int,
        days_left: int,
        airline: str,
        source_city: str,
        departure_time: str,
        stops: str,
        arrival_time: str,
        destination_city: str,
        class_of_flight: str,

        ):

        self.duration = duration
        self.days_left = days_left
        self.airline = airline
        self.source_city = source_city
        self.departure_time = departure_time
        self.stops = stops
        self.arrival_time = arrival_time
        self.destination_city = destination_city
        self.class_of_flight = class_of_flight







    def get_data_as_data_frame(self):
        try:
            custom_data_input = {
                "duration": [self.duration],
                "days_left": [self.days_left],
                "airline": [self.airline],
                "source_city": [self.source_city],
                "departure_time": [self.departure_time],
                "stops": [self.stops],
                "arrival_time": [self.arrival_time],
                "destination_city": [self.destination_city],
                "class": [self.class_of_flight],
            }

            return pd.DataFrame(custom_data_input)

        except Exception as e:
            raise CustomException(e, sys)

