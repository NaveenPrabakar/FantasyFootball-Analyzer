import boto3
import os
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3')

# Upload a file to S3
def upload_file(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path.split('/')[-1]

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {object_name} to {bucket_name}.")
    
    except ClientError as e:
        print(f"Error uploading file {file_path}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Check if a file exists in S3
def check_file_exists(bucket_name, object_name):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
        return True
    
    except ClientError as e:
        # If error code is 404, the file doesn't exist
        if e.response['Error']['Code'] == '404':
            print(f"File {object_name} does not exist in bucket {bucket_name}.")
        else:
            print(f"Error checking file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

# Download a file from S3
def download(bucket_name, object_name):
    try:
        local_dir = "saved_graphs"
        os.makedirs(local_dir, exist_ok=True) 
    
        local_path = os.path.join(local_dir, object_name)

        
        s3_client.download_file(bucket_name, object_name, local_path)
        print(f"Successfully downloaded {object_name} to {local_path}.")
        return local_path
    
    except ClientError as e:
        print(f"Error downloading file {object_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

