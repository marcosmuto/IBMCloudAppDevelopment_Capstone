import requests
import sys
import json
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(dict):
    CLOUDANT_URL=dict["COUCH_URL"]
    CLOUDANT_APIKEY=dict["IAM_API_KEY"]
    DATABASE_NAME='reviews'
    
    authenticator = IAMAuthenticator(CLOUDANT_APIKEY)

    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(CLOUDANT_URL)
    
    # pull all docs
    #response = service.post_all_docs(
    #        db=DATABASE_NAME,
    #        include_docs=True
    #    ).get_result()
    
    dealerSelector = {'$not': {'dealership': 'nil'}}
    if ("dealerId" in dict) :
        dealerId = int(dict["dealerId"])
        dealerSelector = {'dealership': {'$eq': dealerId}}
    
    response = service.post_find(
        db=DATABASE_NAME,
        selector=dealerSelector
    ).get_result()
    
    return response

    