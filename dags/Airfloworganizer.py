from datetime import datetime, timedelta
from Scripts.SaveCommentsTODB import SaveCommentstoDB
from airflow import DAG
from airflow.decorators import task
from Scripts.ParseSavedComments import parseCommentsFromDB
from Scripts.replyToSavedComments import ReplyToComments

with DAG(
    'MuskBot',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='A simple tutorial DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2022, 11, 30),
    catchup=False,
    tags=['example'],
) as dag:
    @task(task_id = "Fetch_Save_comments_toDB")
    def saveComments():
        SaveCommentstoDB()

    @task(task_id = "ParseCommentsTask")
    def parseComments():
        parseCommentsFromDB()
    
    @task(task_id = "ReplyToComments")
    def replyToComment():
        ReplyToComments()

    saveComments() >> parseComments() >> replyToComment()