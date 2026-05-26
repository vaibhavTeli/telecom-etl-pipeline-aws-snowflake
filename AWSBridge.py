import boto3
import os
# --- CREDENTIALS ---
# Note: Hardcoding keys is for Day 1 practice only. 
# In the real world, we use environment variables. Do NOT upload this file to GitHub yet.
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = "telecom-billing-lake-yourname-2026"

print("Initiating connection to AWS S3...")

# Initialize the S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

print(f"Authentication successful. Scanning bucket: {BUCKET_NAME}...\n")

try:
    # Fetch the list of files in your bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' in response:
        print("--- PIPELINE TARGETS FOUND ---")
        for obj in response['Contents']:
            # Print the file name and its size in Megabytes
            file_size_mb = obj['Size'] / (1024 * 1024)
            print(f"File: {obj['Key']} | Size: {file_size_mb:.2f} MB")
        print("------------------------------")
        print("Day 1 Mission Accomplished. The bridge is secure.")
    else:
        print("Connection worked, but the bucket is empty. Go upload your CSV!")

except Exception as e:
    print(f"ACCESS DENIED OR ERROR: {e}")
    print("Check your keys and bucket name.")