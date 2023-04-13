from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from sqlalchemy import text, create_engine
import pandas as pd

file_path = '/tmp/titanic.parquet'
# query_path = '/opt/airflow/path/to/query.sql'
query = '''
SELECT * 
FROM public.titanic
'''

'''
Para criar a tabela titanic_silver, use a query abaixo:
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

def get_table():
    _, con = connect_database(
                                db='harve',
                                user='<usuario>',
                                passwd='<senha>',
                                port='5432'
                            )
    # query = text(open(query_path,'r').read())
    header = con.execute(query).keys()
    data = con.execute(query)
    df = pd.DataFrame(data,columns=header)
    df.to_parquet(file_path,index=False)

def transform():
    df = pd.read_parquet(file_path)
    df['ingested_at'] = datetime.today()

def load():
    engine, con = connect_database(
                                db='harve',
                                user='<usuario>',
                                passwd='<senha>',
                                port='5432'
                            )
    df = pd.read_parquet(file_path)
    df.to_sql( 
        name='titanic_silver',
        con=engine,
        schema='public',
        if_exists='append',
        index=False
    )

with DAG("titanic_etl_dag", 
    description='Extrai os dados do banco, transforma e retorna para outra tabela no banco',
    start_date=datetime(2023,2,14),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    get_table_content = PythonOperator(
        task_id='Get_Table_Content',
        python_callable=get_table
    )

    transform_op = PythonOperator(
        task_id='transform_stuff',
        python_callable=transform
    )

    load_op = PythonOperator(
        task_id='load_stuff',
        python_callable=load
    )

    clean = BashOperator(
        task_id='Delete_Used_Files',
        bash_command=f'rm -f {file_path}'
    )

    get_table_content >> transform_op >>load_op >> clean