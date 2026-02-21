import boto3
import os

# ====== CONFIGURATION ======
bucket_name = 'my-professional-portfolio-2026'  # your S3 bucket name
region_name = 'us-east-1'  # replace if your bucket is in a different region
folder = '.'  # start from current directory (repo root)
# ============================

# Connect to S3
s3 = boto3.client('s3', region_name=region_name)

# Walk through all files in the folder recursively
for root, dirs, files in os.walk(folder):
    for file in files:
        # Skip this script itself
        if file == 'deploy.py':
            continue
        
        local_path = os.path.join(root, file)
        # Compute the relative path to preserve folder structure in S3
        s3_path = os.path.relpath(local_path, folder)
        
        try:
            s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ACL': 'public-read'})
            print(f'✅ Uploaded {s3_path} to S3')
        except Exception as e:
            print(f'❌ Failed to upload {s3_path}: {e}')
