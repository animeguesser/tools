import boto3
import os

def lambda_handler(event, context):
    source_name = os.getenv('SOURCE_BUCKET_NAME')
    target_name = os.getenv('TARGET_BUCKET_NAME')

    # Log into AWS
    session = boto3.Session( aws_access_key_id=os.getenv('ACCESS_KEY'), aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'))
    s3 = session.resource('s3')
    source_bucket = s3.Bucket(source_name)
    target_bucket = s3.Bucket(target_name)

    # Grab all keys from S3
    keys = []
    for obj in source_bucket.objects.all():
        keys.append(obj.key)
    keys.sort()

    # Get first key, split it, and grab the folder out of it
    first = keys[0].split('/')

    # Loop through all keys and only move the 'first' one
    for key in keys:
        if first[0] in key:
            copy_source = {
                'Bucket': source_name,
                'Key': key
            }

            target_bucket.copy(copy_source, f'days/{key}')
            s3.Object(source_name, key).delete()

    

if __name__ == "__main__":
    lambda_handler('a', 'b')