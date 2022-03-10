import requests
import json
from datetime import datetime
from requests.auth import HTTPBasicAuth

review = dict()
review["id"] = int(datetime.now().timestamp())
review["name"] = "Marcos Muto"
review["dealership"] = 1
review["review"] = "Good deal"
review["purchase"] = True
review["purchase_date"] = "02/16/2020"
review["car_make"] = "Honda"
review["car_model"] = "Fit"
review["car_year"] = 2020

print(review)

json_payload = dict()
json_payload["review"] = review

url="https://43bb4759.us-south.apigw.appdomain.cloud/api/review"
    
response = requests.post(url, json=json_payload)
print(response)