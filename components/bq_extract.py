# components/bq_extract.py
from kfp import dsl

# Use your pushed image (has kfp, bigquery, pandas installed)
BASE_IMAGE = "us-central1-docker.pkg.dev/powerful-balm-466923-f4/vertex-feature-docker/vertex-feature:latest"

@dsl.component(base_image=BASE_IMAGE)
def bq_extract(output_csv: dsl.OutputPath(str)):
    """
    Query a tiny public table to stay in the free tier and write a small CSV.
    Forces the job to run in your GCP project and the US multi-region
    (the usa_names public dataset is stored in US).
    """
    from google.cloud import bigquery
    import pandas as pd

    PROJECT_ID = "powerful-balm-466923-f4"  # your project ID
    LOCATION = "US"                         # dataset location for usa_names

    client = bigquery.Client(project=PROJECT_ID)

    sql = """
    SELECT name, gender, state, year, number
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year BETWEEN 2015 AND 2016
    LIMIT 200
    """

    # Ensure the query runs in the correct location and your project
    job = client.query(sql, location=LOCATION)
    df = job.result().to_dataframe(create_bqstorage_client=False)

    df.to_csv(output_csv, index=False)
    print(f"Wrote local artifact CSV at: {output_csv}")