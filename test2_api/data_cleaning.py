import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split
def clean_data(**kwargs):
    # print(kwargs['dag_run'].conf['s3_path'])
    bucket_name = kwargs['dag_run'].conf['bucket_name']
    s3_file_name = kwargs['dag_run'].conf['s3_file_name']
    s3_file_path = "s3://"+bucket_name+"/"+ s3_file_name
    data = pd.read_csv(s3_file_path)
    shape_before = data.shape
    print(data.head())
    print(shape_before)
    data.dropna(inplace = True)
    shape_after = data.shape
    print(shape_before)
    if shape_before!=shape_after:
        print(shape_before[0]-shape_after[0], "Rows dropped from the data")
    shape_before = data.shape
    data = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
    shape_after = data.shape
    if shape_before!=shape_after:
        print(shape_before[0]-shape_after[0], "Rows dropped from the data")
    train,test = train_test_split(data)
    ## Save the processed data to data_folder
    train.to_csv('/home/rahulm/airflow/dags/test2_api/data/wine_train.csv',index = False)
    test.to_csv('/home/rahulm/airflow/dags/test2_api/data/wine_test.csv',index = False)
    return("done")