from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime,timedelta



default_args = {
    'owner': 'Mohamed Eldeeb',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id = "Task_groups",
    default_args = default_args ,
    start_date = datetime(2025,7,1,0,0,0),
    schedule_interval = timedelta(days=1),
    catchup = False
) as dag:
    
    start = DummyOperator(
        task_id = "Starting"
        )
    
    # Task Group for Extraction
    with TaskGroup(
        group_id = "extracting_data_as_a_group",
        tooltip = "Extract Tasks"
    ) as extracting_group:
        task1 = DummyOperator(task_id="extract_from_api")
        task2 = DummyOperator(task_id="extract_from_db")
    
    # Task Group for Transformations    
    with TaskGroup(
        group_id = "trasnforming_data_as_a_group",
        tooltip = "Transform Tasks"
    ) as transforming_group:
        task3 = DummyOperator(task_id="clean_data")
        task4 = DummyOperator(task_id="normalize_data")
    
    end = DummyOperator(task_id="end")
    
start >> extracting_group >> transforming_group >> end