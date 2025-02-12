import os
from dotenv import load_dotenv
from datetime import datetime
from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator

load_dotenv('./envs/.env')

DB_CONFIG = {
    # "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_ENDPOINT"),
    "port": os.getenv("DB_PORT"),
}


with DAG(dag_id = 'test-dag', schedule = None, start_date = datetime(2024, 2, 11)) as dag:
    @task(task_id = 'check_env')
    def check_env_function():
        print(DB_CONFIG)

    @task(task_id = 'print_env')
    def print_env():
        print(os.listdir('./'))

    join_point = EmptyOperator(task_id = 'join_point')


    check_env_function()>>print_env()>>join_point