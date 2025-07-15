from dagster import op
import subprocess

@op
def run_yolo_enrichment():
    subprocess.run(["python", "enrichment/yolo_enrichment.py"], check=True)
