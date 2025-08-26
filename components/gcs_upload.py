# components/gcs_upload.py
from kfp import dsl

BASE_IMAGE = "us-central1-docker.pkg.dev/powerful-balm-466923-f4/vertex-feature-docker/vertex-feature:latest"

@dsl.component(base_image=BASE_IMAGE)
def gcs_upload(input_csv: dsl.InputPath(str), bucket: str, dest_prefix: str) -> str:
    """
    Upload the CSV artifact to GCS at gs://{bucket}/{dest_prefix}/names_sample.csv
    Returns the full gs:// path.
    """
    from google.cloud import storage
    import os

    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    blob_name = f"{dest_prefix.rstrip('/')}/names_sample.csv"
    blob = bucket_obj.blob(blob_name)
    blob.upload_from_filename(input_csv)

    uri = f"gs://{bucket}/{blob_name}"
    print(f"Uploaded to: {uri}")
    return uri