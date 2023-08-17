from flask import Flask, render_template, request
import numpy as np
import pandas as pd
#import logging
#from sklearn.preprocessing import StandardScaler
from src.pipeline.prediction_pipeline import PredictionPipeline, CustomData

application = Flask(__name__,
                    static_folder='static')

app=application

## Routing to home page

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        data=CustomData(
            duration=request.form.get('duration'),
            days_left=request.form.get('days_left'),
            airline=request.form.get('airline'),
            source_city=request.form.get('source_city'),
            departure_time=request.form.get('departure_time'),
            stops=request.form.get('stops'),
            arrival_time=request.form.get('arrival_time'),
            destination_city=request.form.get('destination_city'),
            class_of_flight=request.form.get('class_of_flight')


        )

        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        prediction_pipeline=PredictionPipeline()
        print("During Prediction")
        results = prediction_pipeline.predict(pred_df)
        rounded_results = np.round(results[0], 2)
        print("After Prediction")
        return render_template('home.html',results=rounded_results)
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host="0.0.0.0", port=8080, debug=True) #AWS build
    #app.run(host="0.0.0.0", debug=True) #local - for testing


