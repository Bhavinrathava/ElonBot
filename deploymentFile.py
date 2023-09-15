from datetime import timedelta

import pendulum
from prefect.deployments import DeploymentSpec
from prefect.infrastructure import Process
from prefect.server.schemas.schedules import IntervalSchedule

schedule = IntervalSchedule(
    interval=timedelta(days=1),
    anchor_date=pendulum.datetime(
        2022, 6, 15, 10, 29, 0, tz="America/Chicago"
    ),
)
DeploymentSpec(
    name="elon-bot-dev",
    flow_location="./PrefectDev.py",
    flow_name="ElonBotFlow",
    schedule=schedule,
    flow_runner=Process(),
    tags=["dev"],
)