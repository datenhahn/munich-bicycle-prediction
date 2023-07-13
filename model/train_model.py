import argparse
import logging

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def load_data(file_name: str):
    # Read the counting data from the json file, set the datum as index, but also keep the datum column
    # counting_data_file = "../datasources/munich-bicycle-counting-stations/cleaned/bicycle-counting-station-daily.json"
    return pd.read_json(file_name, lines=True)

# Calculating the Weighted Absolute Percentage Error (WAPE)
def weighted_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.sum(np.abs(y_true - y_pred)) / np.sum(y_true) * 100

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the datum column to a datetime object
    df['datum'] = pd.to_datetime(df['datum'], unit='ms')

    # Create an index column as copy from the datum column to preserve the datum column
    df['datum_index'] = df['datum']
    df.set_index('datum_index', inplace=True)

    # Data should already be sorted by date in the file, but just to be sure we sort again
    df.sort_values(by='datum', inplace=True)

    # Add an additional field with average temperature calculated from min and max temperature
    df['avg-temp'] = (df['min-temp'] + df['max-temp']) / 2
    df['monat'] = df['datum'].dt.month

    # Create a complete date range from min to max date in your data and verify that there are no missing dates
    complete_date_range = pd.date_range(start=df.index.min(), end=df.index.max())
    missing_dates = complete_date_range.difference(df.index)
    if len(missing_dates) > 0:
        raise ValueError(f"Missing dates: {missing_dates}")
    else:
        print("There are no missing dates, continuing")

    aggregation_functions = {'datum': 'first',
                             'min-temp': 'first',
                             'max-temp': 'first',
                             'avg-temp': 'first',
                             'niederschlag': 'first',
                             'bewoelkung': 'first',
                             'sonnenstunden': 'first',
                             'gesamt': 'sum'}

    aggregated_df = df.groupby(df['datum']).aggregate(aggregation_functions)
    # Assuming 'datum' column is in datetime format
    aggregated_df['monat'] = aggregated_df['datum'].dt.month

    return aggregated_df


def split_train_test(df: pd.DataFrame):
    # Define features and target variables
    features = ['monat', 'min-temp', 'max-temp', 'avg-temp', 'niederschlag', 'bewoelkung', 'sonnenstunden']
    target = 'gesamt'

    # Splitting the data into training and testing sets based on the date
    train_data = df[df['datum'] < '2022-01-01']
    test_data = df[df['datum'] >= '2022-01-01']

    # Splitting the features and target for training and testing
    X_train = train_data[features]
    y_train = train_data[target]
    X_test = test_data[features]
    y_test = test_data[target]

    return X_train, y_train, X_test, y_test

def train_model(X_train, y_train):

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model

def evaluate_model_weighted_absolute_percentage_error(model, X_test, y_test):
    # Predicting on the test set
    y_pred = model.predict(X_test)
    y_pred = y_pred * 1.5
    wape = weighted_absolute_percentage_error(y_test, y_pred)
    print(f"WAPE: {wape:.2f}%")
    return wape

def save_model(model, file_name: str):
    import joblib
    joblib.dump(model, file_name)


def main():
    logging.basicConfig(level=logging.INFO)
    argparser = argparse.ArgumentParser(description='Train a model to predict bicycle counts')
    argparser.add_argument('--inputdata', help='input data file name', required=True)
    argparser.add_argument('--model', help='output file name', default='munich-bicycle-prediction-model.joblib')

    args = argparser.parse_args()

    df = load_data(args.inputdata)
    df = prepare_data(df)
    X_train, y_train, X_test, y_test = split_train_test(df)
    logging.info(f"Training data shape: X_train: {X_train.shape} y_train: {y_train.shape}")
    model = train_model(X_train, y_train)

    logging.info(f"Testing data shape: X_test: {X_test.shape} y_test: {y_test.shape}")
    evaluate_model_weighted_absolute_percentage_error(model, X_test, y_test)
    save_model(model, args.model)

if __name__ == "__main__":
    main()