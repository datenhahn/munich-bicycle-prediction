import datetime
from os.path import dirname, abspath
from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from model.model_wrapper import BicyclePredictionModelWrapper, InputFeatures
from openmeteo.meteo import OpenMeteoClient, MUNICH_LAT, MUNICH_LON

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
class Forecast(BaseModel):
    date: datetime.date
    min_temp: float
    max_temp: float
    avg_temp: float
    rain: float
    sun_hours: float
    cloud_cover: float
    bicycle_count: int

client = OpenMeteoClient()
DIR = abspath(dirname(dirname(__file__)))
model = BicyclePredictionModelWrapper(DIR + '/model/munich-bicycle-prediction-model.joblib')

@app.get("/")
async def read_index():
    return FileResponse(DIR + '/webapp/static/index.html')
@app.get("/forecast", response_model=List[Forecast])
async def get_forecast():

    weather_forecast = client.get_7day_forecast(MUNICH_LAT, MUNICH_LON)
    output = []
    for entry in weather_forecast:
        parsed_date = datetime.datetime.fromisoformat(entry['date']).date()
        model_input = InputFeatures(monat=parsed_date.month,
                                 min_temp=entry['min_temp'],
                                 max_temp=entry['max_temp'],
                                 avg_temp=entry['avg_temp'],
                                 niederschlag=entry['rain'],
                                 sonnenstunden=entry['sun_hours'],
                                 bewoelkung=entry['cloud_cover'])
        bicycle_prediction = model.predict(model_input)
        entry['bicycle_count'] = bicycle_prediction
        output.append(Forecast(**entry))

    return output

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)