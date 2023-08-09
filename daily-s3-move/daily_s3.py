import boto3
import os
import json

def lambda_handler(event, context):
    bucket = os.getenv('BUCKET')

    # Log into AWS
    s3_client = boto3.client(
        's3', 
        aws_access_key_id=os.getenv('ACCESS_KEY'), 
        aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'), 
        region_name="us-east-2"
    )
    
    # Get current bucket policy
    response = s3_client.get_bucket_policy(
        Bucket=bucket
    )
    
    # Load bucket policy
    policy = json.loads(response['Policy'])
    policy_resource = policy['Statement'][0]['Resource']

    # Get the next day
    resource_split = policy_resource[-1].split('/')
    next_day = int(resource_split[1]) + 1

    # Update bucket policy with next day
    policy_resource.append(f'{resource_split[0]}/{next_day}/*')

    print(policy_resource)

    # Upload updated policy back to S3
    policy['Statement'][0]['Resource'] = policy_resource
    response = s3_client.put_bucket_policy(
        Bucket=bucket,
        Policy=json.dumps(policy)
    )

if __name__ == "__main__":
    lambda_handler('a', 'b')