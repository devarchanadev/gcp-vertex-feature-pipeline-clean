# src/pipeline/compile_local.py
from kfp import compiler
from src.pipeline.feature_pipeline import bq_to_gcs_pipeline

def main():
    output_path = "pipelines/bq_to_gcs_pipeline.json"
    compiler.Compiler().compile(bq_to_gcs_pipeline, package_path=output_path)
    print(f"Compiled OK → {output_path}")

if __name__ == "__main__":
    main()