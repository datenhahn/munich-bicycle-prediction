"""This module contains the wrapper for the bicycle prediction model."""
import joblib
from sklearn.linear_model import LinearRegression


def load_model(file_name: str) -> LinearRegression:
    """Load the model from the given file name.

    :param file_name: The name of the file containing the model.
    :return: The loaded model.
    """
    return joblib.load(file_name)


class InputFeatures:
    monat: int
    """The month of the forecast."""
    min_temp: float
    """The minimum temperature in °C."""
    max_temp: float
    """The maximum temperature in °C."""
    avg_temp: float
    """The average temperature in °C."""
    niederschlag: float
    """The amount of rain in mm."""
    bewoelkung: float
    """The amount of cloud cover in %."""
    sonnenstunden: float
    """The amount of sun hours."""

    """The InputFeatures represents the input features for the bicycle prediction model."""

    def __init__(self, monat: int, min_temp: float, max_temp: float, avg_temp: float, niederschlag: float,
                 bewoelkung: float, sonnenstunden: float):
        """Initialize the InputFeatures.
        :param monat: The month of the forecast.
        :param min_temp: The minimum temperature in °C.
        :param max_temp: The maximum temperature in °C.
        :param avg_temp: The average temperature in °C.
        :param niederschlag: The amount of rain in mm.
        :param bewoelkung: The amount of cloud cover in %.
        :param sonnenstunden: The amount of sun hours.
        """
        self.monat = monat
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.avg_temp = avg_temp
        self.niederschlag = niederschlag
        self.bewoelkung = bewoelkung
        self.sonnenstunden = sonnenstunden

    def to_list(self) -> list:
        """Return the input features as a list."""
        return [self.monat, self.min_temp, self.max_temp, self.avg_temp, self.niederschlag, self.bewoelkung,
                self.sonnenstunden]

    def __repr__(self):
        """Return a string representation of the InputFeatures."""
        return f"InputFeatures(monat={self.monat}, min_temp={self.min_temp}, max_temp={self.max_temp}, avg_temp={self.avg_temp}, niederschlag={self.niederschlag}, bewoelkung={self.bewoelkung}, sonnenstunden={self.sonnenstunden})"


CORRECTION_FACTOR = 1.5
"""Fixed correction factor for the predicted bicycle count to account for the model having been trained
   with older data, with lower numbers of bicycles.
   This factor was determined by comparing the predicted bicycle counts with the actual bicycle counts. 
"""

class BicyclePredictionModelWrapper():
    """The BicyclePredictionModelWrapper wraps the bicycle prediction model to provide a typed
       interface and to apply the static correction factor to the target variable."""

    model: LinearRegression
    """The actual model."""
    model_file: str
    """The file name of the model."""

    def __init__(self, model_file : str ='./munich-bicycle-prediction-model.joblib'):
        """Initialize the BicyclePredictionModelWrapper.
        
        :param model_file: The file name of the model.
        """
        self.model_file = model_file
        self.model = load_model(model_file)

    def predict(self, features: InputFeatures) -> int:
        """Predict the number of bicycles for the given input features.

        :param features: The input features.
        :return: The predicted number of bicycles.
        """
        return int(self.model.predict([features.to_list()]) * CORRECTION_FACTOR)
