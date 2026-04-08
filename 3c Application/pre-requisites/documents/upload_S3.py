import os
import boto3
from botocore.exceptions import ClientError

REGION = 'us-west-2' # Or your desired region
ACCOUNT_ID = ""
S3_BUCKET_NAME = ""

def create_s3_bucket(s3_client, region, bucket_name):
    """Creates S3 bucket with versioning, encryption, and public access block."""
    print(f"Creating S3 bucket: {bucket_name}...")
    s3_details = {}
    bucket_arn = f"arn:aws:s3:::{bucket_name}"
    try:
        if region == 'us-east-1':
             s3_client.create_bucket(Bucket=bucket_name)
        else:
             s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        print(f"  Bucket {bucket_name} created.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"  Bucket {bucket_name} already exists and is owned by you.")
        elif e.response['Error']['Code'] == 'BucketAlreadyExists':
             raise Exception(f"CRITICAL: Bucket {bucket_name} already exists and is owned by someone else!")
        else: raise

    print("  Configuring bucket properties (Versioning, Encryption, Public Block, Tags)...")
    s3_client.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
    s3_client.put_bucket_encryption(Bucket=bucket_name, ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
    s3_client.put_public_access_block(Bucket=bucket_name, PublicAccessBlockConfiguration={'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True})
    s3_client.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': [{'Key': 'Name', 'Value': bucket_name}]})

def upload_files_to_s3(folder_path, bucket_name, prefix=""):
    # Initialize S3 client
    s3_client = boto3.client('s3')

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Walk through the directory
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            local_path = os.path.join(root, filename)
            
            # Calculate relative path for S3 key
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = os.path.join(prefix, relative_path).replace("\\", "/")

            try:
                # Upload the file to S3
                s3_client.upload_file(local_path, bucket_name, s3_key)
                print(f"Successfully uploaded {relative_path} to {bucket_name}/{s3_key}")
            except ClientError as e:
                print(f"Error uploading {relative_path}: {e}")

if __name__ == "__main__":
    # Folder path
    folder_path = "spec-sheets"
    
    # S3 prefix (optional)
    prefix = "spec-sheets" 

    session = boto3.Session(region_name=REGION)
    sts_client = session.client('sts')
    s3_client = session.client('s3')

    # Get Account ID
    try:
        ACCOUNT_ID = sts_client.get_caller_identity()['Account']
        print(f"AWS Account ID: {ACCOUNT_ID}")
        # Set bucket name now that we have Account ID
        S3_BUCKET_NAME = f"bedrock-kb-{ACCOUNT_ID}-{REGION}" # Unique bucket name
        print(f"Target S3 Bucket Name: {S3_BUCKET_NAME}")
    except ClientError as e:
        raise Exception(f"Could not get AWS Account ID. Check credentials/permissions: {e}")
    
    create_s3_bucket(s3_client, REGION, S3_BUCKET_NAME)

    upload_files_to_s3(folder_path, S3_BUCKET_NAME, prefix)
