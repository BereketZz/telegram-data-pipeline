from dagster import ScheduleDefinition
from orchestration.jobs import data_pipeline

daily_pipeline = ScheduleDefinition(
    job=data_pipeline,
    cron_schedule="0 6 * * *",  # Every day at 6 AM
    name="daily_data_pipeline",
)
