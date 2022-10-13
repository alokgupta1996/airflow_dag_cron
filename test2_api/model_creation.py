import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
model = RandomForestClassifier()
def create_model():
    train_data = pd.read_csv('/home/rahulm/airflow/dags/test2_api/data/wine_train.csv')
    test_data = pd.read_csv('/home/rahulm/airflow/dags/test2_api/data/wine_test.csv')
    X_train,y_train,X_test,y_test = train_data.drop(columns=['quality']),train_data['quality'],test_data.drop(columns=['quality']),test_data['quality']
    mlflow.set_tracking_uri("http://34.199.231.204:7000")
    mlflow.set_experiment("wine_testing")
    with mlflow.start_run() as run:
        n_estimators = 100
        max_depth = 6
        max_features = 3
        # Create and train model
        rf = RandomForestClassifier(n_estimators = n_estimators, max_depth = max_depth, max_features = max_features)
        rf.fit(X_train, y_train)
        # Make predictions
        predictions = rf.predict(X_test)

        # Log parameters
        mlflow.log_param("num_trees", n_estimators)
        mlflow.log_param("maxdepth", max_depth)
        mlflow.log_param("max_feat", max_features)

        # Log model
        mlflow.sklearn.log_model(rf, "random-forest-model")

        # Create metrics
        mse = mean_squared_error(y_test, predictions)

        # Log metrics
        mlflow.log_metric("mse", mse)
        return('model trained')