"""
Customized query with intersight api
https://intersight.com/apidocs/introduction/query/
"""
import os
import intersight.apis
import intersight.authentication

API_KEY_ID = os.getenv("METRIC_API_KEY_ID_V3")
PRIVATE_KEY_FILE = os.getenv("METRIC_API_PRIVATE_KEY_V3")

client = intersight.authentication.get_api_client(api_key_id=API_KEY_ID, api_secret_file=PRIVATE_KEY_FILE, endpoint="https://intersight.com")

compute = intersight.apis.ComputeApi(api_client=client)

# filter query
params = dict(filter="ManagementMode eq 'UCSM'", top=300)
servers = compute.get_compute_physical_summary_list(**params).results

for s in servers:
    print(f"Server: {s.model} | Serial: {s.serial}")