import sys

def main(dict):
    
    return {
        "doc": {
            "id": dict["review"]["id"],
            "name": dict["review"]["name"],
            "dealership": dict["review"]["dealership"],
            "review": dict["review"]["review"],
            "purchase": dict["review"]["purchase"],
            "purchase_date": dict["review"]["purchase_date"],
            "car_make": dict["review"]["car_make"],
            "car_model": dict["review"]["car_model"],
            "car_year": dict["review"]["car_year"]
        }
    }
