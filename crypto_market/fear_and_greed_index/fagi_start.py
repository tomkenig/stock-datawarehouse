# API examples: https://alternative.me/crypto/fear-and-greed-index/
# Example URL: https://api.alternative.me/fng/
# Example URL: https://api.alternative.me/fng/?limit=10
# Example URL: https://api.alternative.me/fng/?limit=10&format=csv
# Example URL: https://api.alternative.me/fng/?limit=10&format=csv&date_format=us


import json
import requests


def get_fagi_data():
    url = "https://api.alternative.me/fng/?limit=10000"
    data = requests.get(url).json()
    return data



print(get_fagi_data())