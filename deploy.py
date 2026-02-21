import boto3
import os
import mimetypes

# ====== CONFIGURATION ======
bucket_name = 'gr-web-html'
region_name = 'us-east-1'
folder = '.'
# ============================

s3 = boto3.client('s3', region_name=region_name)

for root, dirs, files in os.walk(folder):
    for file in files:
        if file == 'deploy.py':
            continue

        local_path = os.path.join(root, file)
        s3_path = os.path.relpath(local_path, folder)

        # Guess content type
        content_type, _ = mimetypes.guess_type(local_path)

        # Default fallback
        if content_type is None:
            content_type = 'application/octet-stream'

        try:
            s3.upload_file(
                local_path,
                bucket_name,
                s3_path,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'public-read'
                }
            )
            print(f'✅ Uploaded {s3_path} ({content_type})')
        except Exception as e:
            print(f'❌ Failed to upload {s3_path}: {e}')