from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime ,timedelta


def push_name_and_age(name,age,ti):
    ti.xcom_push(key="name_age",value=[name,age])
    
def get_name_and_age(ti):
    l  = ti.xcom_pull(task_ids = "add_name_and_age", key ="name_age" )
    print(f"{l[0]} {l[1]}")
    
with DAG(
    dag_id = "xcoms_in_action",
    start_date = datetime(2025,7,1,0,0,0),
    schedule_interval = timedelta(days = 1),
    catchup = False 
)as dag:
    task_1 = PythonOperator(
        task_id = "add_name_and_age",
        python_callable = push_name_and_age,
        op_kwargs = {"name":"moahmed","age":25}
        
    )
    task_2 = PythonOperator(
        task_id = "get_name_and_age",
        python_callable = get_name_and_age
    )
    
task_1 >> task_2