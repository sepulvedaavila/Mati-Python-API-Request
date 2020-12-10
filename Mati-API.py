import requests
import json
import pprint
from base64 import b64encode

CLIENT_ID = "YOUR_CLIENT_ID"
FLOW_ID = "YOUR_FLOW_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET_KEY"


def basic_auth_str(username: str, password: str) -> str:
    auth = b64encode(f'{username}:{password}'.encode('utf-8'))
    return 'Basic ' + auth.decode('ascii')

def authorize():
    url = "https://api.getmati.com/oauth"
    payload = 'grant_type=client_credentials'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': basic_auth_str(CLIENT_ID, CLIENT_SECRET)
    }
    response = json.loads(str(requests.request("POST", url, headers=headers, data=payload).text).split("'")[0])
    access_token = response['access_token']
    return access_token

def create_identity(access_token):
    url = "https://api.getmati.com/v2/verifications"
    payload = '{"flowID": "'+ FLOW_ID +'","metadata": ' \
              '{"key1": "field1", \
                "key2": "field2"}}'
    
    headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    }
    
    response = json.loads(str(requests.request("POST", url, headers=headers, data=payload).text).split("'")[0])

    identity_id = response['identity']
    return identity_id

def send_input(access_token,identity_id, front, back, selfie):
    pp = pprint.PrettyPrinter()
    url = "https://api.getmati.com/v2/identities/{}/send-input".format(identity_id)

    # inputs with Passport + Liveness
    # inputs = '[{"inputType":"document-photo","group":0,"data":{"type":"passport","country":"CU","region":"","page":"front","filename":"passport_3.jpeg"}},{"inputType":"selfie-video","data":{"filename":"selfie_3.mp4"}}]'
    
    # inputs with National ID
    # inputs = '[{"inputType":"document-photo","group": 0,"data":{"type":"national-id","country":"IN","region":"","page":"front","filename":"front.jpg"}},{"inputType":"document-photo","group":0,"data":{"type":"national-id","country":"IN","region": "","page":"back","filename":"back.jpg"}}]'

    # inputs with National ID + Liveness
    inputs = '[{"inputType":"document-photo","group":0,"data":{"type":"national-id","country":"MX","region":"","page":"front","filename":"'+ front +'"}},{"inputType":"document-photo","group":0,"data":{"type":"national-id","country":"MX","region":"","page":"back","filename":"'+ back +'"}},{"inputType":"selfie-video","data":{"filename":"'+ selfie +'"}}]'
    
    payload = {"inputs":inputs}
    
    # open your files corresponding to the ones you declared on the inputs json
    files = [
        ('document', open(front, 'rb')),
        ('document', open(back, 'rb')),
        ('video', open(selfie, 'rb'))
    ]
    
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    
    # print(payload)
    response = requests.request('POST', url, headers=headers, data=payload, files = files)
    #print('Response', response) # 201 + true for each file -> Successful upload

    print(json.loads(response.text.encode('utf8')))

access_token = authorize() # Getting a valid token

front = "front_.jpeg"
back = "back_.jpeg"
selfie = "selfie_.mp4"

identity_id = create_identity(access_token) # Creating the identity and saving the Identity ID
send_input(access_token,identity_id, front, back, selfie) # Sending the data

''' Iterable integration
for x in range(1,16):
    front = "front_"+ str(x) +".jpeg"
    back = "back_"+ str(x) +".jpeg"
    selfie = "selfie_"+ str(x) +".mp4"
    
    identity_id = create_identity(access_token) # Creating the identity and saving the Identity ID
    send_input(access_token,identity_id, front, back, selfie) # Sending the data
'''