from dagster import Definitions
from .jobs import data_pipeline
from .schedules import daily_pipeline

defs = Definitions(
    jobs=[data_pipeline],
    schedules=[daily_pipeline],
)
