FROM apache/airflow:2.4.3

COPY requirement.txt /
COPY --chown=airflow:root Airfloworganizer.py /opt/airflow/dags
COPY --chown=airflow:root ./Scripts/ /opt/airflow/dags/Scripts

RUN pip3 install -r /requirement.txt

