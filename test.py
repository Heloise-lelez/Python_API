import threading
from requests import Session

class TEST():
    def __init__(self):
        self.session = Session()
        self.session.headers ={
            'x-api-key' : "dsq",
        }

        self.base_url = "https://o2t4at65ug.execute-api.eu-west-1.amazonaws.com/dev"

    def get_user(self):
       res = self.session.post(
            url=f"{self.base_url}/userManager",

        )
       
    #    res.raise_for_status()

       print(res.text)


    def create_user(self, email):
       print("Create user")
       res = self.session.post(
            url=f"{self.base_url}/userEmail",
            json={
                "email": email
            }
        )
       print(res.text)

   

test = TEST()
# test.get_user()
test.create_user('')


threads = []
emails = ["111@email.fr", "222@email.fr", "333@email.fr"]



class CustomExcep(Exception):
    def __init__(self, message):
       self.message = message

    def message_Error(self):
        res = {}

        if self.message == "token_error":
            res['body'] = "Wrong Token"
       
        if self.message == "bad_request":
            res['body'] = "Wrong request type"

        if self.message == "mail_error":
            res['body'] = 'Email not found'

        if self.message == "access_environment_error":
            res['body'] = 'Server configuration error'

        return res
    
def tespop():
    try:
       raise CustomExcep("bad_request")
    except CustomExcep as error:
       return error.message_Error()
       
# pop = CustomExcep("bad_request")
# print("pop", pop)