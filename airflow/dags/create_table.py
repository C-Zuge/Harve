from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import text, create_engine
from datetime import datetime

query = '''
create table public.titanic_silver (
    Id_do_passageiro text,
    Sobrevivente text,
    Classe text,
    Nome text,
    Sexo text,
    Idade text,
    Irmaos_ou_conjuge text,
    Pais_ou_filhos text,
    Ticket text,
    Tarifa_do_passageiro text,
    Cabine text,
    Local_de_embarque text,
    Ingested_at date
)
'''

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

def create_table():
    engine, con = connect_database(db='' , user='' , host='' , port='' , passwd='' )
    con.execute(query)

with DAG (
    'create_table',
    start_date=datetime(2023,4,10),
    schedule_interval='@once',
    catchup=False
):
    execute_op = PythonOperator(
        task_id='Create_table',
        python_callable=create_table
    )
    
    execute_op