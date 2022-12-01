FROM apache/airflow:2.4.3

COPY requirements.txt /
COPY --chown=airflow:root Airfloworganizer.py /opt/airflow/dags

RUN pip install --no-cache-dir -r /requirements.txt

