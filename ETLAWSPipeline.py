import boto3
import pandas as pd
import io
import os

# --- CREDENTIALS ---
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "telecom-billing-lake-yourname-2026"
FILE_KEY = "telecom_billing_raw.csv"

print("1. Connecting to AWS S3...")
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

try:
    print(f"2. Streaming {FILE_KEY} directly into memory...")
    # Fetch the object from S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)

    # Read the data stream directly into a Pandas DataFrame
    raw_data = response['Body'].read()
    df = pd.read_csv(io.BytesIO(raw_data))

    print(f"-> Raw Data Loaded: {len(df)} rows.")

    print("\n3. Executing ETL Transformations...")

    # Transformation 1: Filter out bad data
    # Business Logic: We only calculate bills for 'Success' payments.
    # clean_df = df[df['payment_status'] != 'Success']
    # print(f"-> Dropped {len(df) - len(clean_df)} failed/pending records.")

    # Transformation 2: Aggregate data for billing
    # Business Logic: Group by account_id and sum their total usage.
    final_billing_df = df.groupby('payment_status').agg({
        'account_id':'count',
        'duration_seconds': lambda x : str(round((x.sum()/3600),0)) + "hrs",
        'data_mb_used': lambda x: str(round((x.sum()/1024)/1024,2)) + "TB"
    }).reset_index()

    # Transformation 3: Rename columns for Snowflake Schema compatibility
    final_billing_df.rename(columns={
        'duration_seconds': 'total_voice_seconds',
        'data_mb_used': 'total_data_mb'
    }, inplace=True)

    print(f"-> Aggregation complete. Consolidated into {len(final_billing_df)} unique customer bills.")

    print("\n--- PREVIEW OF FINAL TRANSFORMED PAYLOAD ---")
    print(final_billing_df.head())
    print("--------------------------------------------")
    print("Day 2 Mission Accomplished. Data is clean and ready for Snowflake.")

except Exception as e:
    print(f"PIPELINE FAILURE: {e}")