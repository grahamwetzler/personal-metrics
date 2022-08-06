import boto3
import os
import io

access_key_id = os.environ["access_key_id"]
secret_access_key = os.environ["secret_access_key"]
s3_endpoint = os.environ["s3_endpoint"]
bucket_name = os.environ["bucket_name"]


def df_to_parquet_bytes(df):
    file_bytes = io.BytesIO()
    df.to_parquet(file_bytes)
    file_bytes.seek(0)
    return file_bytes


def upload_file(df, file_name):
    s3 = boto3.resource(
        "s3",
        endpoint_url=s3_endpoint,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
    )
    metrics_data_bucket = s3.Bucket(bucket_name)
    file_buffer = df_to_parquet_bytes(df)
    metrics_data_bucket.upload_fileobj(file_buffer, file_name)
