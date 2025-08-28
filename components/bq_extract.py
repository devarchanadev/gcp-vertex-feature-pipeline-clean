# components/bq_extract.py
from kfp import dsl
from kfp.dsl import Dataset, Output  # typed artifacts

# Use your pushed image (has kfp, bigquery, pandas installed)
BASE_IMAGE = "us-central1-docker.pkg.dev/powerful-balm-466923-f4/vertex-feature-docker/vertex-feature:latest"

@dsl.component(base_image=BASE_IMAGE)
def bq_extract(output_csv: Output[Dataset]):
    """
    Query a tiny public table (free) and write a small CSV artifact.
    Forces the job to run in your GCP project and the US multi-region.
    """
    from google.cloud import bigquery
    import pandas as pd

    PROJECT_ID = "powerful-balm-466923-f4"  # your project ID
    LOCATION = "US"                         # usa_names dataset is in US

    client = bigquery.Client(project=PROJECT_ID)
    sql = """
    SELECT name, gender, state, year, number
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year BETWEEN 2015 AND 2016
    LIMIT 200
    """
    job = client.query(sql, location=LOCATION)
    df = job.result().to_dataframe(create_bqstorage_client=False)

    # Write the artifact file
    df.to_csv(output_csv.path, index=False)
    # Optional metadata
    output_csv.metadata["format"] = "csv"
    output_csv.metadata["rows"] = len(df)
    print(f"Wrote CSV artifact at: {output_csv.path}")