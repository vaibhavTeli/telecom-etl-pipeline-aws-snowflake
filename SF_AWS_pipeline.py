import boto3
import pandas as pd
import io
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os

# --- AWS CREDENTIALS ---
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "telecom-billing-lake-yourname-2026"
FILE_KEY = "telecom_billing_raw.csv"

# --- SNOWFLAKE CREDENTIALS ---
SF_ACCOUNT = "UYPKGUD-BDB60349"
SF_USER = "VAIBCODER"
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_WAREHOUSE = "COMPUTE_WH"
SF_DATABASE = "TELECOM_ENTERPRISE"
SF_SCHEMA = "BILLING_DATA"
SF_TABLE = "RAW_CDR_DATA"

print("--- PIPELINE START ---")

# 1. EXTRACT (AWS S3)
print("1. Extracting data from AWS S3...")
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
df = pd.read_csv(io.BytesIO(response['Body'].read()))

# 2. TRANSFORM (Pandas)
print("2. Transforming data (Filtering & Aggregating)...")
clean_df = df[df['payment_status'] == 'Success']

final_billing_df = clean_df.groupby('account_id').agg({
    'duration_seconds': 'sum',
    'data_mb_used': 'sum'
}).reset_index()

final_billing_df.rename(columns={
    'duration_seconds': 'total_voice_seconds',
    'data_mb_used': 'total_data_mb'
}, inplace=True)

# Important for Snowflake: Force column names to UPPERCASE to match the database schema perfectly
final_billing_df.columns = [col.upper() for col in final_billing_df.columns]

# 3. LOAD (Snowflake)
print("3. Connecting to Snowflake Data Warehouse...")
try:
    conn = snowflake.connector.connect(
        user=SF_USER,
        password=SF_PASSWORD,
        account=SF_ACCOUNT,
        warehouse=SF_WAREHOUSE,
        database=SF_DATABASE,
        schema=SF_SCHEMA
    )
    print("-> Connection established.")

    print(f"4. Loading {len(final_billing_df)} records into {SF_TABLE}...")
    # write_pandas is a hyper-optimized function for bulk loading
    success, num_chunks, num_rows, output = write_pandas(conn, final_billing_df, SF_TABLE)

    if success:
        print(f"-> SUCCESS: {num_rows} rows successfully loaded into Snowflake.")
    else:
        print("-> FAILED to load data.")

    conn.close()
    print("--- PIPELINE COMPLETE ---")

except Exception as e:
    print(f"SNOWFLAKE ERROR: {e}")