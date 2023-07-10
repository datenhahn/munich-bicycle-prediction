"""The meteo module provides a client for the OpenMeteo API."""
import pandas as pd
import requests

MUNICH_LAT = 48.1351
"""The latitude of Munich."""

MUNICH_LON = 11.5820
"""The longitude of Munich."""

class MeteoClientException(Exception):
    """An exception raised by the MeteoClient."""
    pass

class OpenMeteoClient:
    """A client for the OpenMeteo API."""
    def __init__(self):
        """Initialize the client."""
        self.base_url = 'https://api.open-meteo.com/v1/forecast'

    def get_hourly_forecast(self, latitude : float, longitude: float, current_weather : bool = False) -> dict:
        """Get the 7 day weather forecast for the given location in hourly resolution.
        :param latitude: The latitude of the location.
        :param longitude: The longitude of the location.
        :param current_weather: Whether to get the current weather additionally to the forecast. (default=False)
        :return: The 7 day weather forecast in hourly steps as a dictionary."""
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': current_weather,
            'hourly': 'temperature_2m,rain,cloudcover,direct_radiation',
            'timezone': 'UTC'
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise MeteoClientException(f'Error while fetching data from OpenMeteo API: {response.status_code} - {response.text}')

    def get_7day_forecast(self, latitude: float, longitude: float) -> list[dict]:
        """Get the 7 day weather forecast for the given location.
        :param latitude: The latitude of the location.
        :param longitude: The longitude of the location."""

        # Retrieve the hourly forecast for the given location
        weather_data = self.get_hourly_forecast(latitude, longitude, current_weather=False)

        # Create a dataframe from the hourly forecast for easier processing
        df = pd.DataFrame({
            'time': weather_data['hourly']['time'],
            'temperature_2m': weather_data['hourly']['temperature_2m'],
            'rain': weather_data['hourly']['rain'],
            'direct_radiation': weather_data['hourly']['direct_radiation'],
            'cloudcover': weather_data['hourly']['cloudcover']
        })

        # Convert 'time' column to datetime format
        df['time'] = pd.to_datetime(df['time'])

        # Resample the dataframe to daily resolution
        df_daily = df.resample('D', on='time')

        # Calculate the daily min, max and average temperature
        min_temp_daily = df_daily['temperature_2m'].min()
        max_temp_daily = df_daily['temperature_2m'].max()
        avg_temp_daily = df_daily['temperature_2m'].mean()

        # The OpenMeteo API does not provide sun hours directly, so as replacement we calculate the daily sun
        # hours by counting the number of hours with direct radiation > 100 W/m^2 .
        # The minimum solar radiation needed to generate electricity is 100-200 W/m2, which is enough to
        # power at least one lamp and fan.
        sun_hours_daily = df[df['direct_radiation'] > 100].resample('D', on='time').size()

        # Calculate the average cloud cover in percent
        avg_cloud_cover_daily = df_daily['cloudcover'].mean()
        avg_rain_daily = df_daily['rain'].mean()

        # Create a new dataframe with the daily min, max and average temperature, sun hours and cloud cover
        df_output = pd.DataFrame()
        df_output['min_temp'] = min_temp_daily
        df_output['max_temp'] = max_temp_daily
        df_output['avg_temp'] = avg_temp_daily
        df_output['rain'] = avg_rain_daily
        df_output['sun_hours'] = sun_hours_daily
        df_output['cloud_cover'] = avg_cloud_cover_daily
        df_output.reset_index(inplace=True)
        df_output.rename(columns={'time': 'date'}, inplace=True)
        df_output['date'] = df_output['date'].dt.strftime('%Y-%m-%d')

        # Return the dataframe as a list of dictionaries for easier processing in the webapp
        return df_output.to_dict(orient='records')
