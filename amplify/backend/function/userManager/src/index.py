from functools import wraps
from http import HTTPStatus
import os
from urllib.error import HTTPError
import boto3

from boto3.dynamodb.conditions import Attr

from wrapper import exeption_handler






#For local testing
# def exeption_handler(func):
#   @wraps(func)
#   def wrapper(event, context):
#     print(event['headers']['x-api-key'])

#     response = {}

#     try:

#         if  not event['headers']['x-api-key']:
#            raise PermissionError("wrong x-api-key")


#         res = func(event, context)
#         if res:
#            response['body'] = json.dumps(res)
#         response['statusCode'] = HTTPStatus.OK

#     except HTTPError as error:
#         response['statusCode'] = error.response.status_code

#     except PermissionError as error:
#             response['body'] = str(error)
#             response['statusCode'] = HTTPStatus.FORBIDDEN

    
#     except Exception as error:
#        response['body'] = str(error)
#        response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR

#     return response
  
#   return wrapper


@exeption_handler
def handler(event, context):
  
  
  print('userManager')
  res = {}
  print(event.get('httpMethod'))
  try : 
    if not event.get('httpMethod') == 'GET':
       raise CustomExcep("bad_request")
  except CustomExcep as error:
    return error.message_Error()
     


  user_table_name= os.environ.get('STORAGE_USERS_NAME')
  dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
  table = dynamodb.Table(user_table_name)

  hashv = event['headers']['x-api-key']



  res = table.scan(
    FilterExpression=Attr('hashValue').eq(hashv),
  )
  print("res : ", res)

  data = res.get('Items')
  print("data : ", data)

  if not data:
     raise CustomExcep("token_error")
  else:
    return data[0].get('email')
  

class CustomExcep(Exception):
    def __init__(self, message):
        self.message = message

    def message_Error(self):
        res = {}

        if self.message == "token_error":
            res['body'] = "Wrong Token"
            res['statusCode'] = HTTPStatus.BAD_REQUEST
       
        if self.message == "bad_request":
            res['body'] = "Wrong request type"
            res['statusCode'] = HTTPStatus.BAD_REQUEST 

        if self.message == "mail_error":
            res['body'] = 'Email not found'
            res['statusCode'] = HTTPStatus.BAD_REQUEST

        if self.message == "access_environment_error":
            res['body'] = 'Server configuration error'
            res['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR

        return res
           
                 
    