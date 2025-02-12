import psycopg2 as pg
from dotenv import load_dotenv
import os
from io import StringIO
import pandas as pd
import numpy as np

load_dotenv('../../envs/.env')

def db_connect(DB_CONFIG):
    try:
        conn = pg.connect(**DB_CONFIG)
        print("Connection succesful!")
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"Connection Failed!\nError: {e}")

def db_close(conn):
    conn.close()

def db_check(db_name):
    DB_CONFIG = {
    # "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_ENDPOINT"),
    "port": os.getenv("DB_PORT"),
    }
    conn = db_connect(DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(f"select 1 from pg_database where datname= %s ;", (db_name, ))
            exists = cur.fetchone()
        db_close(conn)
        if exists:
            print('Database exists.')
            return True
        print('Database does not exist.')
        return False
    except Exception as e:
        print(f'Error with database check.\n Error: {e}')
        print('\n Database does not exist.')
        return False

def create_db(db_name):
    DB_CONFIG = {
    # "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_ENDPOINT"),
    "port": os.getenv("DB_PORT"),
    }
    conn = db_connect(DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(f"create database \"{db_name}\" ;")
            print('Database created!')
    except Exception as e:
        print(f'Failure in creating database\nError: {e}')
    db_close(conn)

def create_tables(DB_CONFIG):
    conn = db_connect(DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(f"""
                create table users(id text primary key not null, name text not null, address text null, phone text null, join_date timestamp, modified_date timestamp);

                create table categories(id text primary key not null, category text not null);

                create table items(id text primary key not null, category_id text not null, item text not null, brand text not null, price_per_unit bigint not null, created_at timestamp, modified_at timestamp, 
                FOREIGN KEY(category_id) references categories(id) on delete cascade
                );
                        
                create table discounts(discount_code text primary key not null, discount_percent bigint not null, discount_type text not null, category_id text null, discount_limit FLOAT8 null, start_date timestamp, end_date timestamp, 
                FOREIGN KEY(category_id) references categories(id) on delete set null);

                create table orders(id text primary key not null, user_id text, order_date timestamp not null, discount_code text null, final_amount FLOAT8 not null, payment_method text, payment_status text, 
                FOREIGN KEY(user_id) references users(id) on delete set null
                );

                create table order_details(id text primary key not null, order_id text not null, item_id text not null, quantity bigint not null, discount_code text null, 
                FOREIGN KEY(order_id) references orders(id) on delete cascade,
                FOREIGN KEY(item_id) references items(id) on delete set null
                );
                """)
        print('Tables Created')
        db_close(conn)
    except Exception as e:
        print(f'Table creation failed!\nError: {e}')

def push_data(DB_CONFIG, df, table_name):
    conn = db_connect(DB_CONFIG)
    try:
        with StringIO() as buffer:
            df = df.applymap(lambda x: None if pd.isna(x) or x == "" else x)
            df.to_csv(buffer, index=False, header=False, sep=",", quotechar='"')
            buffer.seek(0)
            with conn.cursor() as cur:
                cur.copy_from(buffer, table_name, sep=",", columns= df.columns.tolist(), null = "")
        print('Data pushed to table successfully')
        db_close(conn)
    except Exception as e:
        print(f'Data could not be pushed.\nError:{e}')