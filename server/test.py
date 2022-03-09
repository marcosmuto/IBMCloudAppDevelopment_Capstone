import requests
import json
from requests.auth import HTTPBasicAuth

params = dict()
params["text"] = "this is awesome"
params["version"] = "2021-08-01"
params["features"] = "sentiment"
params["return_analyzed_text"] = "return_analyzed_text"
api_key = 'kacv39ZFbEFf1HAVUu0JnsrfQBiNSEMQwjyfzpUkYfFx'
url='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/da0f2ced-9cd4-4264-acc5-e40f7a5d8de7/v1/analyze'
    
response = requests.get(url, 
                headers={'Content-Type': 'application/json'}, 
                auth=HTTPBasicAuth('apikey', api_key),
                params=params)

json_data = json.loads(response.text)
print(json_data["sentiment"]["document"]["label"])