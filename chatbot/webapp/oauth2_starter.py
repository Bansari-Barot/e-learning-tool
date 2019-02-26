# starter code for oauth2 bb RESTapi


import requests
import json

# change user_id and password to current instructor
loginInfo = {
        "user_id": "instructor-1",
        "password": "changeme",
        "action": "login",
        "login": "Login",
    }

payload = {
    'grant_type':'client_credentials'
}

secret = "fKAyn5xtOtd2AK3YUU3qBh6T9n98Qa8i"
key = "e0a2ce49-7e59-4697-9b4d-be9dd53e1cd0"
test_url = "csueastbaysaas-test.blackboard.com"

# taken from https://blackboard.jiveon.com/docs/DOC-1681
def auth_get():
    oauth_path = "/learn/api/public/v1/oauth2/token"
    oauth_url = 'https://' + test_url + oauth_path

    # create new session with credentials, token exp 1 hr
    session = requests.session()
    r = session.post(oauth_url,
                     data = payload,
                     auth=(key, secret),
                     verify = False)

    # print status code and response from token request. 
    print("[auth:setToken()] STATUS CODE: " + str(r.status_code) )
    print("[auth:setToken()] RESPONSE: " + r.text)

    if r.status_code == 200:
        parsed_json = json.loads(r.text)
        token = parsed_json['access_token']
        print("we got a 200 and access token!")

    authStr = 'Bearer ' + token

    # send GET request for instructor information using token
    course_list = session.get('https://csueastbaysaas-test.blackboard.com/'
                              'learn/api/public/v1/users/userName:instructor-1',
                              headers={'Authorization':authStr,
                                       'Content-Type':'application/json'},
                                        verify=False)
    print(course_list.text)

print("Start of set token")
auth_get()
print("End of start token")