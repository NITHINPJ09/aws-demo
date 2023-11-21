import json
import os
import boto3

def lambda_handler(event, context):
    message = 'Hi {}!'.format(event['queryStringParameters']['name'])
    # Retrieve the bucket name from the environment variable
    bucket_name = os.environ.get('S3_BUCKET_NAME')

    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])

        # Process the list of objects
        object_list = [obj['Key'] for obj in objects]

        combined_message = f"{message}, Objects in S3 bucket {bucket_name}: {object_list}"
        response = {
            "statusCode": 200,
            "body": json.dumps({'result': combined_message}),
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({'error': str(e)}),
        }

    return response
