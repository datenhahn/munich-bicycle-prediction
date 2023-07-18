"""The app module provides the web application."""
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

# Add CORS middleware to facilitate local development of the web app.
# See https://fastapi.tiangolo.com/tutorial/cors/
# CAUTION: Tune the CORS settings properly before deploying the web app to production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
class Forecast(BaseModel):
    """The Forecast represents a weather forecast for a single day in Munich
       together with the predicted bicycle count."""

    date: datetime.date
    """The date of the forecast."""
    min_temp: float
    """The minimum temperature in °C."""
    max_temp: float
    """The maximum temperature in °C."""
    avg_temp: float
    """The average temperature in °C."""
    rain: float
    """The amount of rain in mm."""
    sun_hours: float
    """The amount of sun hours."""
    cloud_cover: float
    """The amount of cloud cover in %."""
    bicycle_count: int
    """The predicted bicycle count."""

client = OpenMeteoClient()
DIR = abspath(dirname(dirname(__file__)))
model = BicyclePredictionModelWrapper(DIR + '/model/munich-bicycle-prediction-model.joblib')

@app.get("/")
async def read_index():
    """Serve the index.html file."""
    return FileResponse(DIR + '/webapp/static/index.html')
@app.get("/forecast", response_model=List[Forecast])
async def get_forecast():
    """Return the weather forecast for Munich for the next 7 days together with the predicted bicycle count."""
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
    # Invoke uvicorn directly for easier local development and debugging.
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)