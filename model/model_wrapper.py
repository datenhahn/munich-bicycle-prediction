
import joblib
from sklearn.linear_model import LinearRegression


def load_model(file_name: str) -> LinearRegression:
    return joblib.load(file_name)

class InputFeatures:
    def __init__(self, monat, min_temp, max_temp, avg_temp, niederschlag, bewoelkung, sonnenstunden):
        self.monat = monat
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.avg_temp = avg_temp
        self.niederschlag = niederschlag
        self.bewoelkung = bewoelkung
        self.sonnenstunden = sonnenstunden

    def to_list(self):
        return [self.monat, self.min_temp, self.max_temp, self.avg_temp, self.niederschlag, self.bewoelkung, self.sonnenstunden]
    def __repr__(self):
        return f"InputFeatures(monat={self.monat}, min_temp={self.min_temp}, max_temp={self.max_temp}, avg_temp={self.avg_temp}, niederschlag={self.niederschlag}, bewoelkung={self.bewoelkung}, sonnenstunden={self.sonnenstunden})"

CORRECTION_FACTOR = 1.5
class BicyclePredictionModelWrapper():

    model : LinearRegression
    model_file : str
    def __init__(self, model_file = './munich-bicycle-prediction-model.joblib'):
        self.model_file = model_file
        self.model = load_model(model_file)

    def predict(self, features: InputFeatures) -> int:
        return int(self.model.predict([features.to_list()]) * CORRECTION_FACTOR)
