import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import mlflow
import mlflow.sklearn

def infer_model(**kwargs):
    # print(kwargs['dag_run'].conf['s3_path'])
    bucket_name = kwargs['dag_run'].conf['bucket_name']
    s3_file_name = kwargs['dag_run'].conf['s3_file_name']
    s3_file_path = "s3://"+bucket_name+"/"+ s3_file_name
    test_data = pd.read_csv(s3_file_path)
    # test_data = pd.read_csv('/home/rahulm/airflow/dags/test1/data/wine_test.csv')
    X_test,y_test = test_data.drop(columns=['quality']),test_data['quality']
    mlflow.set_tracking_uri("http://3.6.77.192:7000")
    mlflow.set_experiment("wine_testing_infer")
    with mlflow.start_run():
        #lr = LogisticRegression()
        #lr.fit(X, y)
        model = mlflow.sklearn.load_model("runs:/7f08afa0ddb541069d43db4342ad7734/random-forest-model")
        score = model.score(X_test,y_test)    
        print("Score: %s" % score)
        mlflow.log_metric("score", score)
        #mlflow.sklearn.log_model(lr, "models_dir",registered_model_name="logistics1")
        #print("Model saved in run %s" % mlflow.active_run().info.run_uuid)
    return('Model Infered')