# Import libraries

import argparse
import glob
import os

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

import mlflow

# Construct the tracking URI for MLflow
tracking_uri = (
    "azureml://westeurope.api.azureml.ms/mlflow/v1.0/"
    "subscriptions/80022744-ad47-4e29-838f-f2a430203d84/"
    "resourceGroups/aml_learning_path/"
    "providers/Microsoft.MachineLearningServices/"
    "workspaces/aml_learning_path_1"
)

# Set the tracking URI for MLflow
mlflow.set_tracking_uri(tracking_uri)

# Set the experiment name
mlflow.set_experiment("My-Azure-ML-Experiment")


# define functions
def main(args):
    # TO DO: enable autologging
    mlflow.autolog()

    # read data
    df = get_csvs_df(args.training_data)

    # split data in groups
    X_train, X_test, y_train, y_test = split_data(df)

    # train model
    train_model(args.reg_rate, X_train, X_test, y_train, y_test)


def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


def split_data(df):
    # Define dependent/independent variables
    columns = [
        'Pregnancies', 'PlasmaGlucose', 'DiastolicBloodPressure',
        'TricepsThickness', 'SerumInsulin', 'BMI',
        'DiabetesPedigree', 'Age'
    ]
    X = df[columns].values
    y = df['Diabetic'].values

    # Train/test split function
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=0
    )
    return X_train, X_test, y_train, y_test


def train_model(reg_rate, X_train, X_test, y_train, y_test):
    # train model
    LogisticRegression(C=1/reg_rate, solver="liblinear").fit(X_train, y_train)


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
