from dagster import job
from orchestration.ops.telegram_scraper_op import scrape_telegram_data
from orchestration.ops.load_to_postgres_op import load_raw_to_postgres
from orchestration.ops.dbt_transformation_op import run_dbt_transformations
from orchestration.ops.yolo_enrichment_op import run_yolo_enrichment

@job
def data_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres()
    dbt = run_dbt_transformations()
    yolo = run_yolo_enrichment()

    scrape
    load
    dbt
    yolo
