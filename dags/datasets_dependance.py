"""This code defines three Airflow DAGs that demonstrate dataset dependencies.
The first DAG produces a dataset, the second DAG consumes that dataset to produce another dataset,
and the third DAG reads from the second dataset and prints its contents.
Each DAG is scheduled to run based on the availability of the datasets it depends on.
"""
from airflow.decorators import task, dag
from airflow.datasets import Dataset
import requests as r
import pandas as pd
from datetime import datetime ,timedelta

dataset_1 = Dataset("/opt/airflow/data/output_data/dataset_1.txt")
dataset_2 = Dataset("/opt/airflow/data/output_data/dataset_2.txt")


@dag(schedule_interval = timedelta(days=1),start_date = datetime(2025,1,1,0,0,0),catchup =False)
def dag_a():
    @ task(outlets=[dataset_1])
    def produce_dataset_1():
        with open(dataset_1.uri,"a+") as f:
            f.write("Mohamed , Eldeeb, ECE, 25, DE, moahmedeldeeb@icloud.com \n")
    produce_dataset_1()
dag_a()

@dag(schedule = [dataset_1],start_date = datetime(2025,1,1,0,0,0),catchup =False)
def dag_b():
    @task(outlets = [dataset_2])
    def produce_dataset_2_from_dataset_1():
        with open(dataset_1.uri,"r") as fi:
            data = fi.read()
        with open(dataset_2.uri,"a+") as fo:
            fo.write(data + "Mustafa , Eldeeb, CS, 22, SWE, mustafaeldeeb@icloud.com"+ "\n")
    produce_dataset_2_from_dataset_1()
dag_b()


@dag(schedule = [dataset_2],start_date = datetime(2025,1,1,0,0,0),catchup =False)
def dag_c():
    @task
    def get_data():
        data =  pd.read_csv(dataset_2.uri, header=None)
        print(data)
    get_data()
dag_c()