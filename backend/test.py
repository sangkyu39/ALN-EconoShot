import json
import os
from pprint import pprint
import requests

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
subscription_key = "fb7ae6af50954d659d9a3ff86e8afe4e"  # API key from environment
endpoint = "https://api.bing.microsoft.com/v7.0/news/search"  # Correct endpoint for news search

# Query term(s) to search for
query = "Microsoft"

# Construct a request
mkt = 'ko-KR'
params = {'q': query, 'mkt': mkt, 'count': 10}  # You can specify 'count' to limit the number of results
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

# Call the API
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("Headers:")
    print(response.headers)

    print("JSON Response:")
    pprint(response.json())
except Exception as ex:
    raise ex
