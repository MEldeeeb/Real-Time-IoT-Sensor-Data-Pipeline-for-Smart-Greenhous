from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset
from airflow.decorators import task
from datetime import datetime , timedelta

my_dataset = Dataset("/opt/airflow/data/output_data/text.txt") 

def update_my_file():
        with open(my_dataset.uri, "a+") as f: # note you can get the uri of the dataset
            f.write("updating the file \n")  


def read_my_file():
    with open(my_dataset,"r") as f:
        print(f.read())



# -------------------------- producer_dag -------------------------- #
with DAG(
    dag_id = "producer_dag",
    start_date =  datetime(2025,6,30,0,0,0),
    schedule_interval = timedelta(days=1) , 
    catchup = False
)as dag:
    task_1 = PythonOperator(
        task_id = "update_task",
        python_callable = update_my_file ,
        outlets = [my_dataset]  # this tells airflow that the python called in this task is updating a dataset 
    )

task_1


# -------------------------- consumer_dag -------------------------- #
with DAG(
    dag_id = "consumer_dag",
    start_date = datetime(2025,7,1,0,0,0),
    schedule = [my_dataset], 
    catchup = False
) as dag:
    task_2 = PythonOperator(
        task_id = "get_the_update",
        python_callable = read_my_file
    )
task_2