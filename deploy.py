import boto3
import os

# Get AWS credentials from environment variables (Jenkins will pass these)
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']

# Replace with your actual S3 bucket name
bucket_name = 'grace-professional-portfolio-2026'

# Local folder to upload (repo root)
local_folder = "."

# Connect to S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Upload files
for root, dirs, files in os.walk(local_folder):
    for file in files:
        if file.endswith(('.html', '.css')):  # Only upload HTML & CSS
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, local_folder)
            print(f"Uploading {local_path} to s3://{bucket_name}/{s3_path}")
            s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ACL':'public-read'})

print("Deployment to S3 completed successfully!")
