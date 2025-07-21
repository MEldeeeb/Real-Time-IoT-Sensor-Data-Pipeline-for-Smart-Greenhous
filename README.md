# Real-Time AgriTech Data Pipeline for Smart Greenhouses


## Description

**Real-Time AgriTech Data Pipeline for Smart Greenhouses** powered by an end-to-end real-time **data pipeline**.

The system simulates IoT sensor data, including temperature, humidity, air quality, and soil moisture, using **Python** to reflect realistic greenhouse conditions.  
Each sensor streams data into a unified **Apache Kafka** topic, with producers and consumers handling ingestion and initial processing.  

Incoming data is **validated and enriched** with metadata before being stored in an **Operational Data Store (ODS)** using **PostgreSQL** for real-time monitoring.  

For historical insights and strategic decision-making:
- Processed data is modeled in a **star schema** and loaded into **Snowflake** (EDWH).
- Raw data is archived in **HDFS** to support batch processing.
- **Apache Spark** runs nightly aggregation jobs to analyze daily sensor trends and generate **automated email reports** for stakeholders.



## System Architecture

![System Architecture](./images/Full%20Architecture.png)



## Logical Components

### 1. Data Sources

**IoT Sensors**  
Devices that generate real-time data (temperature, humidity, air quality, soil moisture).

- **Input Format:** JSON

```json
{
  "sensor_id": "string",
  "timestamp": "string",
  "sensor_type": "string",
  "value": "float",
  "location": "string"
}
```



## Ingestion Layer

**Apache Kafka**
- Acts as the real-time data ingestion and messaging backbone.
- Each sensor type writes to a dedicated Kafka topic (e.g., `temperature`, `air_quality`, `humidity`).

---

## Processing Layer

**Real-Time Processing**
- **Python Kafka Consumer:**
  - Reads messages from Kafka topics.
  - Validates and enriches data with metadata (e.g., standardized timestamps, location codes).

**Batch Processing**
- **Apache Spark on HDFS:**
  - Runs nightly batch jobs to aggregate sensor data by:
    - Region
    - Sensor type
    - Time intervals (daily, weekly)
  - Generates reports and summary tables.



## Storage Layer

- **Data Lake (Raw Data):**
  - **HDFS** archives unprocessed IoT sensor data for:
    - Historical analysis
    - Reprocessing scenarios

- **Data Warehouse (Processed Data):**
  - **Snowflake:** Stores cleaned, modeled data for analytics and dashboards.
  - **PostgreSQL:** Stores current real-time data for monitoring applications.

---

## Analytics, Visualization, & Reporting

- **Visualization:**
  - Real-time KPIs like active sensors and current readings.
  - Historical trends and aggregated metrics.
  - **Power BI** dashboards for exploration and reporting.

- **Reporting:**
  - Daily automated email reports to stakeholders with summarized sensor trends and anomalies.

---

## Schema

![Schema](/images/Schema.png)

---

## Future Work

- **Docker** containerization of all services to improve:
  - Deployment consistency
  - Scalability
  - Portability
- Full **workflow orchestration with Apache Airflow** to automate:
  - Spark aggregation jobs
  - ETL pipelines (ODS → Snowflake)
  - Report generation and distribution

---

## High-Level Data Flow

1. **Data Generation:**
   - IoT sensors send data as JSON messages to Kafka.
2. **Ingestion:**
   - Kafka brokers distribute data across topics and partitions.
3. **Processing:**
   - Python consumers transform and validate data in real time.
   - Spark jobs perform daily batch aggregations.
4. **Storage:**
   - Raw data is archived in HDFS.
   - Cleaned data is saved to PostgreSQL and Snowflake.
5. **Visualization:**
   - Power BI dashboards fetch insights from the warehouse.
6. **Reporting:**
   - Automated emails deliver daily summaries to stakeholders.





# 🐳 Dockerized Data Engineering Stack

A fully integrated Docker-based environment for building modern data engineering pipelines with:

- **Apache Airflow**
- **Apache Kafka + Zookeeper**
- **Apache Hadoop (HDFS + YARN)**
- **PostgreSQL (Airflow & Application)**
- **Jupyter Notebook with PySpark**



## 🔧 Services Summary
#### 🌐 Internal Network Configuration
All containers are connected to the custom Docker bridge network `sparknet` with a static IP setup in the `172.30.0.0/16` subnet

| Service                  | Description                                         | Container Name        | Internal IP     | Host IP     | Port Mapping                   | Username     | Password     |
|--------------------------|-----------------------------------------------------|------------------------|------------------|-------------|-------------------------------|--------------|--------------|
| **Airflow Webserver**    | Airflow UI and REST API                             | `airflow-webserver`    | `172.30.1.15`    | `localhost` | `18080:8080`                   | `airflow`    | `airflow`    |
| **Airflow Scheduler**    | DAG execution engine                                | `airflow-scheduler`    | `172.30.1.16`    | Internal    | -                             | `airflow`    | `airflow`    |
| **Airflow Triggerer**    | Async task handler                                  | `airflow-triggerer`    | `172.30.1.17`    | Internal    | -                             | `airflow`    | `airflow`    |
| **Airflow CLI**          | Airflow terminal commands                           | `airflow-cli`          | `172.30.1.20`    | Internal    | -                             | `airflow`    | `airflow`    |
| **Airflow Init**         | DB initialization + user bootstrap                  | `airflow-init`         | `172.30.1.18`    | Internal    | -                             | `airflow`    | `airflow`    |
| **PostgreSQL (Airflow)** | Metadata DB for Airflow                             | `postgres_airflow`     | `172.30.1.14`    | Internal    | -                             | `airflow`    | `airflow`    |
| **PostgreSQL (App)**     | General-purpose app DB                              | `postgres_v2`          | `172.30.1.12`    | `localhost` | `5433:5432`                   | `spark`      | `spark`      |
| **Zookeeper**            | Kafka coordination                                  | `zookeeper_v2`         | `172.30.1.10`    | `localhost` | `2181:2181`                   | N/A          | N/A          |
| **Kafka**                | Kafka broker for stream ingestion                   | `kafka_v2`             | `172.30.1.11`    | `localhost` | `9092`, `19092:19092`         | N/A          | N/A          |
| **Jupyter Notebook**     | PySpark-enabled notebook environment                | `spark-jupyter`        | `172.30.1.13`    | `localhost` | `8899:8888`, `4040:4040`      | N/A          | N/A          |
| **Hadoop NameNode**      | Master node for HDFS                                | `hadoop-namenode`      | `172.30.1.21`    | `localhost` | `9870:9870`, `9000:9000`      | N/A          | N/A          |
| **Hadoop DataNode 1**    | HDFS data storage node                              | `hadoop-datanode1`     | `172.30.1.22`    | `localhost` | `9864:9864`, `9866`, `9867`   | N/A          | N/A          |
| **Hadoop DataNode 2**    | HDFS data storage node                              | `hadoop-datanode2`     | `172.30.1.23`    | Internal    | `9865`, `9868`, `9869`        | N/A          | N/A          |
| **ResourceManager**      | YARN job scheduling                                 | `hadoop-resourcemanager`| `172.30.1.24`    | `localhost` | `8088:8088`                   | N/A          | N/A          |
| **NodeManager**          | YARN container execution                            | `hadoop-nodemanager`   | `172.30.1.25`    | Internal    | -                             | N/A          | N/A          |



## 🔗 Web Interfaces

| Component                 | URL                                   | Notes                                |
|---------------------------|----------------------------------------|--------------------------------------|
| **Airflow UI**            | [http://localhost:18080](http://localhost:18080) | Use `airflow/airflow` to log in     |
| **Jupyter Notebook (Lab)**| [http://localhost:8899](http://localhost:8899)   | No token required                    |
| **Spark UI**              | [http://localhost:4040](http://localhost:4040)   | Visible during active Spark jobs    |
| **HDFS NameNode UI**      | [http://localhost:9870](http://localhost:9870)   | File system browser                  |
| **YARN ResourceManager**  | [http://localhost:8088](http://localhost:8088)   | Job monitoring & container status   |






## 📦 Docker Volumes

These ensure **persistent storage**:

| Volume Name         | Used By           | Purpose                      |
|---------------------|-------------------|------------------------------|
| `postgres-db-volume`| `postgres_airflow`| Airflow metadata DB          |
| `pgdata`            | `postgres`        | Application PostgreSQL DB    |
| `hadoop-namenode`   | `hadoop-namenode` | HDFS NameNode metadata       |
| `hadoop-datanode1`  | `hadoop-datanode1`| HDFS DataNode 1 data         |
| `hadoop-datanode2`  | `hadoop-datanode2`| HDFS DataNode 2 data         |




## 📁 Project Folder Structure

```text
.
├── dags/             ← Airflow DAGs
├── logs/             ← Airflow logs
├── config/           ← Optional Airflow configs
├── plugins/          ← Custom Airflow plugins
├── data/             ← Input/output data folder
├── notebooks/        ← Jupyter notebooks
├── jars/             ← Spark JARs (for Kafka, MongoDB, etc.)
├── docker-compose.yml
└── file.md           ← This documentation

```
## Connect with me

- [🔗 LinkedIn Account  →    WWW.linkedin.com/mohamed-eldeeb](https://www.linkedin.com/in/mohamed-eldeeb-9706261b6/)
