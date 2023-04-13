from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import requests
import io

filePath = '/tmp/titanic.parquet'

def connect_database(db, user, host, port, passwd):
    """
    Get SQLalchemy engine using credentials.
    Input:
    db: database name
    user: Username
    host: Hostname of the database server
    port: Port number
    passwd: Password for the database
    """

    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    engine = create_engine(url)
    con = engine.connect()
    return engine, con

def extract():
    url = 'https://www.harve.com.br/praticas/titanic-pt-BR.csv'
    response = requests.get(url)
    buffer = io.StringIO(response.text)
    df = pd.read_csv(buffer)
    df.to_parquet(filePath,index=False)

def transform():
    df = pd.read_parquet(filePath)
    renameColumns = {column:column.strip().replace(' ','_').lower() for column in df.columns}
    df.rename(columns=renameColumns,inplace=True)
    df['ingested_at'] = datetime.today()
    df.to_parquet(filePath,index=False)

def load():
    engine, con = connect_database(
                                db='',
                                user='',
                                passwd='',
                                host='',
                                port='5432'
                            )
    
    df = pd.read_parquet(filePath)
    con.execute('''truncate table public.titanic_silver''')
    df.to_sql( 
        name='titanic_silver',
        con=engine,
        schema='public',
        if_exists='append',
        index=False
    )

with DAG('cesar_etl',
    description='minha primeira dag de etl no airflow',
    start_date = datetime(2023,4,11),
    schedule_interval='@daily',
    catchup=False
):
    extract_op = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    transform_op = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    load_op = PythonOperator(
        task_id='load',
        python_callable=load
    )

    extract_op >> transform_op >> load_op