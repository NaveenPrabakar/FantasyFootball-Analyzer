import boto3
import os
from botocore.exceptions import ClientError
import pymysql

# Initialize S3 client
s3_client = boto3.client('s3')


#AWS RDS Config:
RDS_HOST = os.getenv("HOST")
RDS_PORT = 3306
RDS_USER = os.getenv("username")
RDS_PASSWORD = os.getenv("AWS_RDS")
RDS_DB_NAME = "ndlvideodb"

# Establish connection to AWS RDS
def connect_to_rds_mysql():
    
    try:
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME,
            port=RDS_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Successfully connected to MySQL RDS instance.")
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL RDS: {e}")
        return None

#Create a table
def create_table(connection):
   
    create_table_query = """
    CREATE TABLE IF NOT EXISTS PlayerVideos (
        player VARCHAR(255) PRIMARY KEY,
        video VARCHAR(255) NOT NULL
    );
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'PlayerVideos' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

#Insert into tabke
def insert_data(connection, player, video):
    insert_query = """
    INSERT INTO PlayerVideos (player, video)
    VALUES (%s, %s);
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(insert_query, (player, video))
            connection.commit()
            print(f"Inserted ({player}, {video}) into PlayerVideos.")
    except Exception as e:
        print(f"Error inserting data: {e}")

#Query
def get_player_videos(connection, player_name):

    select_query = """
    SELECT video FROM PlayerVideos WHERE player = %s;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_query, (player_name,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


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
        local_dir = "tmp/saved_graphs"
        os.makedirs(local_dir, exist_ok=True) 
    
        local_path = os.path.join(local_dir, object_name)

        
        s3_client.download_file(bucket_name, object_name, local_path)
        print(f"Successfully downloaded {object_name} to {local_path}.")
        return local_path
    
    except ClientError as e:
        print(f"Error downloading file {object_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

