import psycopg2 as pg
import pandas as pd
import boto3
import io
import dataBaseOps
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv('../../envs/.env')


def extract_and_transform_data(view_name, query_path):
    DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_ENDPOINT"),
    "port": os.getenv("DB_PORT"),
    }
    try:   
        conn = dataBaseOps.db_connect(DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(
            f"""
            SELECT EXISTS (
            SELECT 1
            FROM information_schema.views
            WHERE table_schema = 'public'  -- Or your schema name
            AND table_name = '{view_name}'
            );
            """
            )
            exists = cur.fetchone()
        dataBaseOps.db_close(conn)
        print('View exists.')
    except:
        print('View does not exist')
        exists = False
        dataBaseOps.db_close(conn)
    conn = dataBaseOps.db_connect(DB_CONFIG)
    with conn.cursor() as cur:  
        if exists:
            cur.execute(
                f"""
                select * from {view_name};
                """        
            )
            print('View fetched.')  
            return pd.DataFrame(columns = [desc[0] for desc in cur.description], data = cur.fetchall())
        with open(query_path) as f:
            view_query_if_not_exists = f.read()
        cur.execute(
            f"""
            create view {view_name} as
            {view_query_if_not_exists}
            select * from {view_name};
            """
            )
        print("View created.")
        return pd.DataFrame(columns = [desc[0] for desc in cur.description], data = cur.fetchall())

def load_table_to_s3(df, view_name):
    try:
        session = boto3.Session(
        region_name= os.getenv("REGION_NAME"),
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY")
        )
        s3 = session.client(service_name='s3')
        print('Connection success')
    except Exception as e:
        print(f'Connection Failed.\nError: {e}')
        
    try:
        with io.BytesIO() as buffer:
            df.to_csv(buffer, index = None)
            buffer.seek(0)
            s3.upload_fileobj(buffer, os.getenv("BUCKET_NAME"), f"{view_name}{date.today()}.csv")
            print('File Uploaded.')
    except Exception as e:
        print(f"Write Failed\nError: {e}")   
    

