import boto3
import os

# Replace this with your actual S3 bucket name
bucket_name = 'grace-digital-portfolio-2026'
folder = 'Digital Portfolio/'

# Connect to S3
s3 = boto3.client('s3')

# Upload each file in the folder
for root, dirs, files in os.walk(folder):
    for file in files:
        local_path = os.path.join(root, file)
        s3_path = os.path.relpath(local_path, folder)
        s3.upload_file(local_path, bucket_name, s3_path)
        print(f'Uploaded {file} to S3')