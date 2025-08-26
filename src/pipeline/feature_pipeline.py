# src/pipeline/feature_pipeline.py
from kfp import dsl
from components.bq_extract import bq_extract
from components.gcs_upload import gcs_upload

@dsl.pipeline(name="bq-to-gcs-features")
def bq_to_gcs_pipeline(bucket: str, dest_prefix: str = "features/usa_names_sample"):
    """
    Minimal BigQuery -> CSV -> GCS pipeline.
    - bucket: your target GCS bucket name (no gs://)
    - dest_prefix: folder/prefix within the bucket
    """
    extract_task = bq_extract()
    upload_task = gcs_upload(
        input_csv=extract_task.outputs["output_csv"],
        bucket=bucket,
        dest_prefix=dest_prefix
    )
    # Optionally, you can print or use upload_task.output (the gs:// URI) downstream