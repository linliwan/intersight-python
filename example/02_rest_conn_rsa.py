"""
    Use Intersight's API key v2 (based on RSA private key) to initiate REST requests
    Just for the convenience of learning and understanding
    Please use Intersight python sdk directly in production
    Author: Linlin Wang
"""

import requests
import base64
import hashlib
from email.utils import formatdate
from urllib.parse import urlparse
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from pprint import pprint
import os

API_KEY_ID = os.getenv("INTERSIGHT_API_KEY_ID_V2")
PRIVATE_KEY_FILE = os.getenv("INTERSIGHT_API_PRIVATE_KEY_V2")

def generate_auth_headers(api_key_id, private_key_file, method, url, body=""):
    # Read RSA private key
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

    # Parse the URL. For example, for "https://intersight.com/api/v1/compute/PhysicalSummaries", the parsing result is:
    # ParseResult(scheme='https', netloc='intersight.com', path='/api/v1/compute/PhysicalSummaries', params='', query='', fragment='')
    parsed_url = urlparse(url)
    path = parsed_url.path
    query = parsed_url.query
    host = parsed_url.netloc
    full_path = f"{path}?{query}" if query else path

    method = method.upper()

    if isinstance(body, str):
        body = body.encode("utf-8")
    digest = "SHA-256=" + base64.b64encode(hashlib.sha256(body).digest()).decode()
    # Hash the request body with SHA-256, then encode it with Base64 to form the digest
    # Even for GET requests, the digest must be calculated (even if the body is empty)

    timestamp = formatdate(usegmt=True)

    # Construct signature string
    signed_headers = [
        f"(request-target): {method.lower()} {full_path}",
        f"host: {host}",
        f"date: {timestamp}",
        f"digest: {digest}"
    ]
    signature_string = "\n".join(signed_headers).encode("utf-8")
    # Concatenate several key fields (in a fixed order) into the "string to be signed". 
    # This step must be done in full accordance with Cisco requirements. 
    # The field name, order, and format must not be wrong.

    # Sign using RSA PKCS1v15
    # Intersight will use your public key to verify whether the signature is legal.
    signature = base64.b64encode(
        private_key.sign(signature_string, padding.PKCS1v15(), hashes.SHA256())
    ).decode()

    # Construct the authorization header
    auth_header = (
        f'Signature keyId="{api_key_id}",'
        f'algorithm="hs2019",'
        f'headers="(request-target) host date digest",'
        f'signature="{signature}"'
    )

    return {
        "Date": timestamp,
        "Digest": digest,
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }

# Example call
url = "https://intersight.com/api/v1/compute/PhysicalSummaries"
headers = generate_auth_headers(API_KEY_ID, PRIVATE_KEY_FILE, "GET", url)

print("===------------------------- HEADERS -------------------------===")
pprint(headers)
print("===-----------------------------------------------------------===")

# Making a request and handling the response
response = requests.get(url, headers=headers)
servers = response.json()['Results']

for server in servers:
    print(f"Server: {server['Model']} | Serial: {server['Serial']}")
