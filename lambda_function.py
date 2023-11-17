import json
import logging
import boto3
import botocore
from botocore.exceptions import ClientError

def get_presigned_url(bucket_name, object_name, expiration=600):

    # Generate a presigned URL for the S3 object
    print("Generating get URL!")
    s3_client = boto3.client('s3',region_name="us-east-1")
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name
                                                    },
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        logging.error(e)
        return "Error"

    # The response contains the presigned URL
    return response
    
def put_presigned_url(bucket_name, object_name, expiration=600):

    # Generate a presigned URL for the S3 object
    print("Generating put URL!")
    s3_client = boto3.client('s3',region_name="us-east-1")
    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name,
                                                            'ContentType': 'application/octet-stream'
                                                    },
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        logging.error(e)
        return "Error"

    # The response contains the presigned URL
    return response
    

def lambda_handler(event, context):
    request = event.get("body")
    if not request:
        return {
            'statusCode': 404,
            'body': "Wrong request"
        }
    body = json.loads(request)
    print("Body: " + str(body))
    if body.get("type") == "PUT":
        responce = put_presigned_url("target-bucket-test-123", body["fileName"], 3600)
        print("URL: " + responce)
        return {
            'statusCode': 200,
            'body': responce
        }
    elif body.get("type") == "GET":
        responce = get_presigned_url("target-bucket-test-123", body["fileName"], 3600)
        print("URL: " + responce)
        return {
            'statusCode': 200,
            'body': responce
        }
    else:
        return {
            'statusCode': 404,
            'body': "No such type"
        }
