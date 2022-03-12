import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    has_api_key = "api_key" in kwargs
    try:
        # Call get method of requests library with URL and parameters
        if has_api_key:
            api_key = kwargs["api_key"]
            params = kwargs["params"]
            response = requests.get(url, 
                headers={'Content-Type': 'application/json'}, 
                auth=HTTPBasicAuth('apikey', api_key),
                params=params)
        else:
            response = requests.get(url, 
                headers={'Content-Type': 'application/json'}, 
                params=kwargs)
    except Exception as excep:
        # If any error occurs
        print("Network exception occurred:")
        print(excep)

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    print(payload)
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, 
            json=payload,
            params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["data"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"], 
                city=dealer["city"], 
                full_name=dealer["full_name"],
                id=dealer["id"], 
                lat=dealer["lat"], 
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"], 
                state=dealer["state"], 
                zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result["docs"]
        
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                id=review["id"],
                name=review["name"],
                dealership=review["dealership"],
                review=review["review"],
                purchase=review["purchase"],
		        purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"], 
                sentiment = analyze_review_sentiments(review["review"])
                )

            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    params = dict()
    params["text"] = dealerreview
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = "return_analyzed_text"
    
    api_key = '#IBM_CLOUD_NLU_API_KEY#'
    if os.getenv('VCAP_APPLICATION'):
        api_key = os.getenv('IBM_CLOUD_NLU_API_KEY')

    url='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/da0f2ced-9cd4-4264-acc5-e40f7a5d8de7/v1/analyze'

    json_result = get_request(url, params=params, api_key=api_key)

    print(json_result)

    response = "neutral"

    try: 
        if "sentiment" in json_result:
            response = json_result["sentiment"]["document"]["label"]
        elif "error" in json_result:
            #response = json_result["error"]
            response = "neutral"
    except:
        # If any error occurs
        #response = "Error trying to analyze the sentiment"
        response = "neutral"

    return response

