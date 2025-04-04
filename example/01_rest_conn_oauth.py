"""
    Use Intersight's OAuth2 client credentials to initiate REST requests
    Just for the convenience of learning and understanding
    Please use Intersight python sdk directly in production
    Author: Linlin Wang
"""

import requests
from pprint import pprint
import os

# Read from environment variables for security
CLIENT_ID = os.getenv("INTERSIGHT_API_OAUTH2_ID")
CLIENT_SECRET = os.getenv("INTERSIGHT_API_OAUTH2_SECRET")

# Token endpoint for OAuth2
TOKEN_URL = "https://intersight.com/iam/token"

# If you consider it comprehensively, you should use cache to cache tokens. 
# Before getting a new token each time, check whether the token in the cache is expired. 
# This script is simplified and does not design cache.
# _token_cache = {"token": None, "expires_at": 0}

def get_access_token(client_id, client_secret):
    """
    Use client credentials (client_id & client_secret) to obtain an access token
    """
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(TOKEN_URL, data=payload)

    if response.status_code == 200:
        print("===------------------------- RESPONSE: access_token -------------------------===")
        pprint(response.json())
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to obtain access token: {response.status_code}, {response.text}")

# A example call
url = "https://intersight.com/api/v1/compute/PhysicalSummaries"

# First, get the access token
access_token = get_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Construct the authorization header
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

print("===------------------------- HEADERS -------------------------===")
pprint(headers)
print("===-----------------------------------------------------------===")

# Make the API request using the access token
response = requests.get(url, headers=headers)
servers = response.json()['Results']

for server in servers:
    print(f"Server: {server['Model']} | Serial: {server['Serial']}")
