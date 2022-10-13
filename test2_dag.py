import datetime as dt
from airflow import DAG
from airflow.models import DagRun
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
# from .data_cleaning import clean_data
from test2_api.data_cleaning import clean_data
from test2_api.model_creation import create_model
from test2_api.inference import infer_model
# Say this is Task1
def greet(**kwargs):
    '''
    A python function to write a text file
    '''
    print('Writing in file')
    # print(kwargs['dag_run'].conf['s3_path'])
    # print(kwargs["s3_path"])

    with open('greet.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        f.write(str(t) + '\n')
    return "greeted"
# Say this is task2
def respond():
    '''
    A python function to return a simple greetingthon function to return a simple greeting
    '''
    return 'Greet Responded Again'
# Declaring DAG default settings
default_args = {
    'owner': 'rahul',
    'start_date': dt.datetime(2022, 9, 14, 10, 00, 00),
    'concurrency': 1,
    'retries': 0
}
# Building the DAG, 'my_simple_dag' is the dag id, which will be
# visible in the airflow ui
with DAG('trigger_test_sample',
         catchup=False,
         default_args=default_args,
        #  schedule_interval='*/30 * * * *',
         schedule_interval=None,
         ) as dag:
    # print(default_args)
    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')
    opr_greet = PythonOperator(task_id='greet',
                               python_callable=greet)
    opr_clean = PythonOperator(task_id='clean_data',
                               python_callable=clean_data)
    opr_model = PythonOperator(task_id='create_model',
                               python_callable=create_model)
    opr_infer = PythonOperator(task_id='infer_model',
                               python_callable=infer_model)
    opr_sleep = BashOperator(task_id='sleep_me',
                             bash_command='sleep 5')
    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
    # Setting the task flow dependencies
    opr_hello >> opr_greet >> opr_clean >> opr_model >> opr_infer >> opr_sleep >> opr_respond
