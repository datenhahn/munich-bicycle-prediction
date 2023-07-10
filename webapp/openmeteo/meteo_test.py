from datetime import datetime, timedelta
import json

from openmeteo.meteo import OpenMeteoClient, MUNICH_LAT, MUNICH_LON


def test_integration_should_download_and_parse_data_when_called_with_location_of_munich():
    """Test that the OpenMeteoClient returns the expected data for Munich."""

    # GIVEN: The OpenMeteoClient and the location of Munich.
    client = OpenMeteoClient()

    # WHEN: We the forecast is requested.
    weather_data = client.get_7day_forecast(MUNICH_LAT, MUNICH_LON)

    # THEN: It should return a list of dictionaries with the expected keys and valid values.
    assert len(weather_data) == 7
    assert type(weather_data) == list
    for entry in weather_data:
        assert type(entry) == dict
        # The values are in the expected range.
        assert entry['min_temp'] > -30.0 and entry['min_temp'] < 45.0
        assert entry['max_temp'] > entry['min_temp']
        assert entry['avg_temp'] > entry['min_temp'] and entry['avg_temp'] < entry['max_temp']
        assert entry['rain'] >= 0 and entry['rain'] <= 10000
        assert entry['sun_hours'] >= 0 and entry['sun_hours'] <= 20
        assert entry['cloud_cover'] >= 0 and entry['cloud_cover'] <= 100
        assert type(entry['date']) == str
        parsed_date = datetime.fromisoformat(entry['date']).date()
        assert parsed_date >= datetime.today().date() and parsed_date <= datetime.today().date() + timedelta(days=6)

    with open('test_data.json', 'w') as f:
        f.write(json.dumps(weather_data))
