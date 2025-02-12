from datetime import datetime
import sys
import os
from dotenv import load_dotenv
import pandas as pd
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

load_dotenv('./envs/.env')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../customScripts/pythonScripts')))

DB_CONFIG = {
    # "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_ENDPOINT"),
    "port": os.getenv("DB_PORT"),
}

with DAG(dag_id = "retailDataPipeline", start_date = datetime(2025, 2, 10), schedule = None) as dag:
    
#check_db->if exists->runquery->storeins3
#check_db->if not exists->create db->create tables->generate data->push data->runquery->storeins3
    say_hello = BashOperator(
        task_id = 'start_task',
        bash_command = 'echo "Hello!"',
        dag = dag
    )
    say_goodbye = BashOperator(
        task_id = 'end_task',
        bash_command = 'echo "Pipeline successful! Goodbye!"',
        dag = dag
    )

    join_point = EmptyOperator(task_id = 'join_point', trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)

    @task.branch(task_id = 'check_db_task')
    def check_db_existence():
        from dataBaseOps import db_check
        if db_check('retail_db'):
            return 'join_point'
        return 'create_db_task'
    
    @task(task_id = 'create_db_task')
    def create_new_database():
        from dataBaseOps import create_db
        DB_CONFIG['dbname'] = os.getenv("DB_NAME")
        return create_db(DB_CONFIG['dbname'])
    
    @task(task_id = 'create_tables_task')
    def create_all_tables():
        from dataBaseOps import create_tables
        DB_CONFIG['dbname'] = os.getenv("DB_NAME")
        return create_tables(DB_CONFIG)
    


    @task(task_id = 'generate_and_push_data_task')
    def generate_and_push_data_to_rds():
        from dataBaseOps import push_data
        import dataGenerator as dgen
        df_dictionary = dict()
        df_dictionary['users'] = dgen.user_generator(7500)
        df_dictionary['categories'], df_dictionary['items'] = dgen.category_item_generator()
        df_dictionary['discounts'] = dgen.discount_generator(df_dictionary['categories']['id'], 2000)
        df_dictionary['orders'], df_dictionary['order_details'] = dgen.order_generator(user_df=df_dictionary['users'], discount_df=df_dictionary['discounts'], item_df=df_dictionary["items"], n=50000)
        DB_CONFIG['dbname'] = os.getenv("DB_NAME")
        for i in df_dictionary:
            push_data(DB_CONFIG=DB_CONFIG, df = df_dictionary[i], table_name=i)


    @task(task_id = 'transformation_task')
    def transform_data():
        from ETL import extract_and_transform_data
        view_dir = os.listdir('./customScripts/sqlScripts')
        views = [f.replace('.txt', '') for f in view_dir if os.path.isfile(os.path.join('./customScripts/sqlScripts', f)) ]
        for i in views:
            df = extract_and_transform_data(i, os.path.join('./customScripts/sqlScripts', f"{i}.txt"))
            df.to_csv(os.path.join('./temp', f"{i}.csv"))

    @task(task_id = 'store_data_task')
    def store_data():
        from ETL import load_table_to_s3
        temp_dir = os.listdir('./temp')
        temp_files = [f for f in temp_dir if os.path.isfile(os.path.join('./temp', f))]
        for i in temp_files:
            df = pd.read_csv(os.path.join('./temp', i))
            load_table_to_s3(df, i.replace('.csv', ''))

    @task(task_id = 'cleanup_task')
    def folder_cleanup():
        folder_path = os.listdir('./temp')
        temp_files = [f for f in folder_path if os.path.isfile(os.path.join('./temp', f))]
        for i in temp_files:
            os.remove(os.path.join('./temp', i))
    

    t1 = say_hello
    t2 = check_db_existence()
    t3 = create_new_database()
    t4 = create_all_tables()
    t5 = generate_and_push_data_to_rds()
    t6 = join_point
    t7 = transform_data()
    t8 = store_data()
    t9 = folder_cleanup()
    t10 = say_goodbye

    t1>>t2

    t2>>t3>>t4>>t5>>t6

    t2>>t6

    t6>>t7>>t8>>t9>>t10
        

    




