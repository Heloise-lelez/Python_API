import os
import boto3


def handler(event, context):

    user_table_name= os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)

    table.put_item(
        Item={
            'id': event['user_id'],
            'email': event['user_email'],
            'hashValue': event['hashValue']
        })
    
    print('email added')
