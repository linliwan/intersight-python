"""
Reference: https://github.com/CiscoDevNet/intersight-python
"""
import os
import intersight.apis
import intersight.authentication

API_KEY_ID = os.getenv("INTERSIGHT_API_KEY_ID_V3")
PRIVATE_KEY_FILE = os.getenv("INTERSIGHT_API_PRIVATE_KEY_V3")

client = intersight.authentication.get_api_client(api_key_id=API_KEY_ID, api_secret_file=PRIVATE_KEY_FILE, endpoint="https://intersight.com")

compute = intersight.apis.ComputeApi(api_client=client)
servers = compute.get_compute_physical_summary_list().results

for server in servers:
    print(f"Server: {server.model} | Serial: {server.serial}")

