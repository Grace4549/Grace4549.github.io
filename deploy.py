import argparse
import boto3
import mimetypes
import os

# ====== CONFIGURATION ======
bucket_name = 'gr-web-html'  # your S3 bucket name
region_name = 'us-east-1'  # replace if your bucket is in a different region
folder = '.'  # start from current directory (repo root)
# ============================

parser = argparse.ArgumentParser(description='Upload static site to S3 with correct metadata')
parser.add_argument('--dry-run', action='store_true', help='Print uploads without sending to S3')
args = parser.parse_args()

# Connect to S3
s3 = boto3.client('s3', region_name=region_name)

# Initialize mime types
mimetypes.init()

def should_skip(path, filename):
    # Skip this script, python cache, hidden files, and common VCS dirs
    if filename == os.path.basename(__file__):
        return True
    if filename.endswith('.pyc') or filename == '.DS_Store':
        return True
    if any(part.startswith('.') for part in path.split(os.sep)):
        return True
    if any(part in ('__pycache__', '.git', 'node_modules') for part in path.split(os.sep)):
        return True
    return False

# Walk through all files in the folder recursively
for root, dirs, files in os.walk(folder):
    for file in files:
        if should_skip(root, file):
            continue

        local_path = os.path.join(root, file)
        # Compute the relative path to preserve folder structure in S3
        s3_path = os.path.relpath(local_path, folder).replace(os.sep, '/')

        # Guess content type
        content_type, _ = mimetypes.guess_type(local_path)

        extra_args = {'ACL': 'public-read'}
        if content_type:
            extra_args['ContentType'] = content_type

        if args.dry_run:
            print(f"DRY-RUN: {local_path} -> {s3_path} | ExtraArgs={extra_args}")
            continue

        try:
            s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs=extra_args)
            print(f'✅ Uploaded {s3_path} to S3 (Content-Type: {extra_args.get("ContentType")})')
        except Exception as e:
            print(f'❌ Failed to upload {s3_path}: {e}')
