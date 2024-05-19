import base64
import hashlib
import hmac
import json
import config
import requests

# username = config.username
# password = config.password
# authUrl = config.priaid_authservice_url
# healthUrl = config.priaid_healthservice_url
# language = config.language
# printRawOutput = config.pritnRawOutput

# print(username)
# print(password)
# print(authUrl)

def load_token(username, password, url):
    # Compute the hash using HMAC MD5 (Note: you can change this to SHA256 if needed)
    rawHashString = hashlib.md5(url.encode('utf-8')).hexdigest()
    computedHashString = base64.b64encode(rawHashString.encode('utf-8')).decode()

    # rawHashString = hmac.new(bytes(password, encoding='utf-8'), authUrl.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # computedHashString = base64.b64encode(rawHashString).decode()

    bearer_credentials = username + ':' + computedHashString
    postHeaders = {
            'Authorization': 'Bearer {}'.format(bearer_credentials)
    }

    print("RAW HASH STRING: " + str(rawHashString))
    print("COMPUTED HASH STRING: " + computedHashString)
    print("HEADERS: " + postHeaders["Authorization"])

    responsePost = requests.post(url, headers=postHeaders)
    
    # Check if the request was successful
    responsePost.raise_for_status()

    print("===================================================")
    print(responsePost.text)
    print("===================================================")

    data = json.loads(responsePost.text)
    print(data['Token'])

    return data






# def __init__(self, username, password, authServiceUrl, language, healthServiceUrl):
#     self._handleRequiredArguments(username, password, authServiceUrl, healthServiceUrl, language)

#     self._language = language
#     self._healthServiceUrl = healthServiceUrl
#     self._token = self._loadToken(username, password, authServiceUrl)


# def _loadToken(self, username, password, url):
#     rawHashString = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8')).digest()
#     computedHashString = base64.b64encode(rawHashString).decode()

#     bearer_credentials = username + ':' + computedHashString
#     postHeaders = {
#             'Authorization': 'Bearer {}'.format(bearer_credentials)
#     }
#     responsePost = requests.post(url, headers=postHeaders)

#     data = json.loads(responsePost.text)
#     return data