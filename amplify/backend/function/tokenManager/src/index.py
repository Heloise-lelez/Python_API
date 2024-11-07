import uuid
import boto3
import os
import json
import hmac
import hashlib

from http import HTTPStatus
from boto3.dynamodb.conditions import Key


def handler(event, context):
    response = {}
   
# check if the request is the right type
    try : 
        if not event.get('httpMethod') == 'POST':
         raise CustomExcep("bad_request")
    except CustomExcep as error:
        return error.message_Error()
        

    user_table_name= os.environ.get('STORAGE_USERS_NAME')
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(user_table_name)

    user_id = str(uuid.uuid4())
    print(user_id)


    # Seach if there is email ad body in event
    user_email = None
    try:
        if not event['body']:
            raise CustomExcep("body_error")
        
        user_email = json.loads(event['body']).get('email')

        if not user_email:
            raise CustomExcep("mail_error")
        

        
    except CustomExcep as error:
        return error.message_Error()
        
    
    
    combined_values = f"{user_id}{user_email}"
    hashValue = hmac.new(user_id.encode(), combined_values.encode(), hashlib.sha256).hexdigest()
    print("hashValue" , hashValue)  

    #search if email is already known in db

    res = table.query(
                IndexName='emails',   
                KeyConditionExpression=Key('email').eq(user_email)
            )
    

    #If email doesn't exists, add email on db

    if not res['Items']:
        user_create_func = os.environ.get('FUNCTION_USERCREATE_NAME')

        if not user_create_func:
            raise CustomExcep("access_environment_error")

        client = boto3.client('lambda', region_name='eu-west-1')

        payload = {
            "user_id": user_id,
            "user_email": user_email,
            "hashValue": hashValue
        }

        invoke_res = client.invoke(
            FunctionName=user_create_func,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print(invoke_res)

        response['body'] = user_id
        response['statusCode']=HTTPStatus.OK
    else:
        print('email already known')
        user_id = res['Items'][0].get('id')
        response['body'] = user_id
        response['statusCode']=HTTPStatus.OK

    return response


class CustomExcep(Exception):
    def __init__(self, message):
        self.message = message

    def message_Error(self):
        res = {}

        if self.message == "token_error":
            res['body'] = "Wrong Token"
            res['statusCode'] = HTTPStatus.BAD_REQUEST
        
        if self.message == "bad_request":
            res['body'] = "Bad Request"
            res['statusCode'] = HTTPStatus.BAD_REQUEST 

        if self.message == "mail_error":
            res['body'] = 'Email required'
            res['statusCode'] = HTTPStatus.BAD_REQUEST

        if self.message == "body_error":
            res['body'] = 'Body not found'
            res['statusCode'] = HTTPStatus.BAD_REQUEST

        if self.message == "access_environment_error":
            res['body'] = 'Server configuration error'
            res['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR

        return res
           
                 
    