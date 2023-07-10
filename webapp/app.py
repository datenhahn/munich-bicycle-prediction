import joblib
import uvicorn as uvicorn
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import datetime

from starlette.middleware.cors import CORSMiddleware

from model.train_model import ModelInput
from openmeteo.meteo import OpenMeteoClient, MUNICH_LAT, MUNICH_LON

def load_model(file_name: str):
    return joblib.load(file_name)

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

model = load_model('munich-bicycle-prediction-model.joblib')

@app.get("/forecast", response_model=List[Forecast])
async def get_forecast():

    weather_forecast = client.get_7day_forecast(MUNICH_LAT, MUNICH_LON)
    output = []
    for entry in weather_forecast:
        parsed_date = datetime.datetime.fromisoformat(entry['date']).date()
        model_input = ModelInput(monat=parsed_date.month,
                                 min_temp=round(entry['min_temp'],1),
                                 max_temp=round(entry['max_temp'],1),
                                 avg_temp=round(entry['avg_temp'],1),
                                 niederschlag=round(entry['rain'],1),
                                 sonnenstunden=round(entry['sun_hours'],1),
                                 bewoelkung=round(entry['cloud_cover'],1))
        bicycle_prediction = model.predict([model_input.to_list()])
        entry['bicycle_count'] = int(bicycle_prediction[0])
        output.append(Forecast(**entry))

    return output

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)