import json
from requests import HTTPError
from functools import wraps
from http import HTTPStatus

def exeption_handler(func):
  @wraps(func)
  def wrapper(event, context):
    print("wrapper")
    # print(event['headers']['x-api-key'])
    print(event)

    response = {}

    try:

        if not event['headers'].get('x-api-key'):
           raise PermissionError("wrong x-api-key")


        res = func(event, context)
        if res:
           response['body'] = json.dumps(res)
        response['statusCode'] = HTTPStatus.OK

    except HTTPError as error:
        response['statusCode'] = error.response.status_code

    except PermissionError as error:
            response['body'] = str(error)
            response['statusCode'] = HTTPStatus.FORBIDDEN

    
    except Exception as error:
       response['body'] = str(error)
       response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR

    return response
  
  return wrapper
