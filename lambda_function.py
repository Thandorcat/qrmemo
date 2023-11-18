import json
import logging
import boto3
import botocore
import os 
from botocore.exceptions import ClientError

S3_TARGET_BUCKET = os.environ.get('target_bucket')

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

def generate_existing_file(item, secret_provided):
    secret_stored = item['secret']
    path = item['path']

    if secret_provided != secret_stored:
        return {
            'statusCode': 401,
            'body': "Wrong secret!"
        }

    presigned_url = get_presigned_url(S3_TARGET_BUCKET, path, 3600)
    print("URL: " + presigned_url)
    data = {
        'url': presigned_url,
        'existing_file': True,
    }

    resourse = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }
    return resourse

def generate_new_file(table, token, secret_provided):
    path = token + '/' + 'image.jpg'
    item = {
        'token': token,
        'secret': secret_provided,
        'path': path
    }
    
    response = table.put_item(Item=item)
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        return {
            'statusCode': 500,
            'body': "Something wrong DB"
        }

    presigned_url = put_presigned_url(S3_TARGET_BUCKET, path, 3600)
    data = {
        'url': presigned_url,
        'existing_file': False,
    }

    resourse = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(data)
    }
    return resourse

def lambda_handler(event, context):
    request = event.get("body")
    if not request:
        return {
            'statusCode': 404,
            'body': "Wrong request!"
        }
    body = json.loads(request)
    print("Body: " + str(body))

    token = body.get("token")
    secret_provided = body.get("secret")
    if not token or not secret_provided:
        return {
            'statusCode': 404,
            'body': "Wrong parameters!"
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tokens')
    primary_key_value = {'token': token}
    response = table.get_item(Key=primary_key_value)

    # Check if record exists
    if 'Item' in response:
        print("Record exists" + str(response['Item']))
        item = response['Item']
        response = generate_existing_file(item, secret_provided)
        return response
    else:
        response = generate_new_file(table, token, secret_provided)
        return response
