from dagster import op
import subprocess

@op
def load_raw_to_postgres():
    subprocess.run(["python", "etl/load_raw_to_postgres.py"], check=True)
