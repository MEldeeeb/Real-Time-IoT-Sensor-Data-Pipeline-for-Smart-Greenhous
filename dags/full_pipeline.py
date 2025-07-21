from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sensors.base import BaseSensorOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests 
from datetime import datetime
from datetime import timedelta


DDL_db = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY, 
            user_f_name VARCHAR(50),
            user_l_name VARCHAR(50),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) """

def get_data_from_api():
    responce = requests.get("https://raw.githubusercontent.com/marclamberti/datasets/refs/heads/main/fakeuser.json")
    if responce.status_code == 200:
        return responce.json() # This will be stored in XCom automatically in case of calling from a python operator task 
    else:
        return None


def extract_user(ti):
    fake_user = ti.xcom_pull(task_ids = "get_data_from_api")
    if fake_user is not None:
        return{
            "id" : fake_user["id"],
            "user_f_name" : fake_user["personalInfo"]["firstName"],
            "user_l_name" : fake_user["personalInfo"]["lastName"],
            "email" : fake_user["personalInfo"]["email"]
        }
    else:
        return None
    
    
    
def process_user_data(ti):
    user_data = ti.xcom_pull(task_ids = "extract_user")
    if user_data is not None:
        return f"{user_data['id']},{user_data['user_f_name']},{user_data['user_l_name']},{user_data['email']}"
    else:
        return None



def save_user_data_to_csv(ti):
    data = ti.xcom_pull(task_ids = "process_user_data") 
    if data is not None:
        with open("/opt/airflow/data/output_data/User_data_out.csv","w") as f:
            f.write(data)
    else:
        return None


def store_user_data_into_PG_db():
    hook = PostgresHook(postgres_conn_id = "postgeres_conn")
    sql = """
        COPY users (user_id, user_f_name, user_l_name, email)
        FROM STDIN WITH CSV
    """
    hook.copy_expert(sql = sql , filename = "/opt/airflow/data/output_data/User_data_out.csv")
    
    
    
# ------------------------------------ DAG  ------------------------------------ #
with DAG(
    dag_id = "users_activity_pipeline",
    start_date = datetime(2025,7,1,0,0,0),
    schedule_interval = timedelta(days = 1),
    catchup = False 
)as dag:
    
    # Task to create a table in PostgreSQL
    create_users_table = SQLExecuteQueryOperator(
        task_id = "create_users_table",
        conn_id = "postgeres_conn",
        sql = DDL_db
    )
    
    # Task to check API availability
    check_api_availability = PythonOperator(
        task_id = "get_data_from_api",
        python_callable = get_data_from_api  
    )
    
    # Task to extract user data from the API response
    get_user_data = PythonOperator(
        task_id = "extract_user",
        python_callable = extract_user
    )
    
    # Task to process user data
    process_user = PythonOperator(
        task_id = "process_user_data",
        python_callable = process_user_data
    )
    
    # Task to save user data into a CSV file
    save_into_csv = PythonOperator(
        task_id  = "append_user_data_to_csv",
        python_callable = save_user_data_to_csv
    )
    
    # Task to load users dataa into a postgres db 
    load_to_db = PythonOperator(
        task_id = "storing_users_data_into_pg_db",
        python_callable  = store_user_data_into_PG_db
    )
    
create_users_table >> check_api_availability >> get_user_data >> process_user >> save_into_csv >> load_to_db