"""
    This script is used to restore the Standalone UCSC CIMC device connector to factory settings.
    Cisco officially provides a PowerShell-based script.
    https://www.cisco.com/c/en/us/support/docs/servers-unified-computing/integrated-management-controller/221002-reset-device-connector-to-factory-with-p.html

    This script is adapted based on the official PowerShell version to facilitate Python users. 
    Please read the official documentation carefully before using it.

    This script is for learning and research only.
    Author: Linlin Wang
"""

import requests
from xml.etree import ElementTree
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

CIMC_IP = "192.168.17.8"
USERNAME = "admin"
PASSWORD = "admin"

login_url = f"https://{CIMC_IP}/nuova"
device_connector_url = f"https://{CIMC_IP}/connector/DeviceConnections"

def login(username, password):
    payload = f"<aaaLogin inName='{username}' inPassword='{password}' />"
    response = requests.post(login_url, data=payload, verify=False)
    response.raise_for_status()
    xml = ElementTree.fromstring(response.content)
    cookie = xml.attrib.get('outCookie')
    if not cookie:
        raise Exception("[Login failed], can not obtain cookie")
    print(f"[Login Result]: cookie - {cookie}")
    return cookie

def get_cloud_dns(cookie):
    headers = {'ucsmcookie': f'ucsm-cookie={cookie}'}
    response = requests.get(device_connector_url, headers=headers, verify=False)
    response.raise_for_status()
    data = response.json()[0]
    print("[Current CloudDns]:", data.get("CloudDns"))
    return data

def update_cloud_dns(cookie, new_intersigit_addr):
    headers = {'ucsmcookie': f'ucsm-cookie={cookie}'}
    body = {
        "CloudDns": new_intersigit_addr,
        "ForceResetIdentity": True,
        "ResetIdentity": True
    }
    response = requests.put(device_connector_url, headers=headers, json=body, verify=False)
    response.raise_for_status()
    print(f"[Update Result]: {response}")

def logout(cookie):
    payload = f"<aaaLogout inCookie='{cookie}' />"
    response = requests.post(login_url, data=payload, verify=False)
    response.raise_for_status()
    print(f"[Logout Result]: {response}")


if __name__ == "__main__":
    cookie = login(USERNAME, PASSWORD)
    get_cloud_dns(cookie)
    update_cloud_dns(cookie, "svc.intersight.com")
    logout(cookie)
