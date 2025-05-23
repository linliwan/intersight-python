"""
    A minimal code example using the intersight python SDK
    Customized query with intersight api
    Author: Linlin Wang
"""

import os
import intersight.apis
import intersight.authentication
import csv

API_KEY_ID = os.getenv("METRIC_API_KEY_ID_V3")
PRIVATE_KEY_FILE = os.getenv("METRIC_API_PRIVATE_KEY_V3")

client = intersight.authentication.get_api_client(api_key_id=API_KEY_ID, api_secret_file=PRIVATE_KEY_FILE, endpoint="https://intersight.com")

compute = intersight.apis.ComputeApi(api_client=client)

# A example with how to use keyword args of intersight api
# Specifies the maximum number of resources to return in the response, refer to the source code of this function
servers = compute.get_compute_physical_summary_list(top=300).results

with open("servers.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Model", "Serial", "ManagementMode"])
    for s in servers:
        writer.writerow([s.name, s.model, s.serial, s.management_mode])
        # if s.serial == "FCH250671GR":
        #     print(s)



### The following is a complete output example for a single server ###

# {'account_moid': '59bc454c16267c000192f683',
#  'admin_power_state': '',
#  'alarm_summary': {'class_id': 'compute.AlarmSummary',
#                    'critical': 0,
#                    'health': 'Healthy',
#                    'info': 0,
#                    'object_type': 'compute.AlarmSummary',
#                    'suppressed': False,
#                    'suppressed_critical': 0,
#                    'suppressed_info': 0,
#                    'suppressed_warning': 0,
#                    'warning': 0},
#  'ancestors': [{'class_id': 'mo.MoRef',
#                 'link': 'https://intersight.com/api/v1/equipment/Chasses/67ea92456176753301c60ad6',
#                 'moid': '67ea92456176753301c60ad6',
#                 'object_type': 'equipment.Chassis'}],
#  'asset_tag': '',
#  'available_memory': 512,
#  'bios_post_complete': True,
#  'chassis_id': '1',
#  'class_id': 'compute.PhysicalSummary',
#  'connection_status': '',
#  'cpu_capacity': 145.59999,
#  'create_time': datetime.datetime(2025, 4, 1, 11, 21, 41, 712000, tzinfo=tzutc()),
#  'custom_permission_resources': [{'class_id': 'mo.MoRef',
#                                   'link': 'https://intersight.com/api/v1/organization/Organizations/5ddeb51e6972652d30b7fb0a',
#                                   'moid': '5ddeb51e6972652d30b7fb0a',
#                                   'object_type': 'organization.Organization'},
#                                  {'class_id': 'mo.MoRef',
#                                   'link': 'https://intersight.com/api/v1/organization/Organizations/67d946ef697265300102cf5a',
#                                   'moid': '67d946ef697265300102cf5a',
#                                   'object_type': 'organization.Organization'},
#                                  {'class_id': 'mo.MoRef',
#                                   'link': 'https://intersight.com/api/v1/organization/Organizations/67470bd06972653001275553',
#                                   'moid': '67470bd06972653001275553',
#                                   'object_type': 'organization.Organization'}],
#  'device_mo_id': '67ebcc086f72613201338329',
#  'dn': '/redfish/v1/Systems/FCH250671GR',
#  'domain_group_moid': '5b25418c7a7662743465cf4c',
#  'equipment_chassis': {'class_id': 'mo.MoRef',
#                        'link': 'https://intersight.com/api/v1/equipment/Chasses/67ea92456176753301c60ad6',
#                        'moid': '67ea92456176753301c60ad6',
#                        'object_type': 'equipment.Chassis'},
#  'fault_summary': 0,
#  'firmware': '5.3(0.250001)',
#  'front_panel_lock_state': 'Lock',
#  'hardware_uuid': 'F2BA6D4B-0EAC-488A-94AB-6891A2E4C0F0',
#  'inventory_device_info': None,
#  'inventory_parent': {'class_id': 'mo.MoRef',
#                       'link': 'https://intersight.com/api/v1/equipment/Chasses/67ea92456176753301c60ad6',
#                       'moid': '67ea92456176753301c60ad6',
#                       'object_type': 'equipment.Chassis'},
#  'ipv4_address': '127.0.0.1',
#  'is_upgraded': False,
#  'kvm_ip_addresses': [{'address': '198.19.223.181',
#                        'category': 'Equipment',
#                        'class_id': 'compute.IpAddress',
#                        'default_gateway': '198.19.216.1',
#                        'dn': '',
#                        'http_port': 80,
#                        'https_port': 443,
#                        'kvm_port': 2068,
#                        'kvm_vlan': 0,
#                        'name': 'Outband',
#                        'object_type': 'compute.IpAddress',
#                        'subnet': '255.255.248.0',
#                        'type': 'MgmtInterface'}],
#  'kvm_server_state_enabled': True,
#  'kvm_vendor': 'Cisco Systems',
#  'lifecycle': 'Active',
#  'management_mode': 'Intersight',
#  'memory_speed': '3200',
#  'mgmt_ip_address': '198.19.223.181',
#  'mod_time': datetime.datetime(2025, 4, 5, 6, 20, 0, 27000, tzinfo=tzutc()),
#  'model': 'UCSX-210C-M6',
#  'moid': '67ebcc456176753301d03c84',
#  'name': 'lon-ai1-pod1-1-6',
#  'num_adaptors': 1,
#  'num_cpu_cores': 56,
#  'num_cpu_cores_enabled': 56,
#  'num_cpus': 2,
#  'num_eth_host_interfaces': 1,
#  'num_fc_host_interfaces': 0,
#  'num_threads': 112,
#  'object_type': 'compute.PhysicalSummary',
#  'oper_power_state': 'on',
#  'oper_reason': [],
#  'oper_state': '',
#  'operability': '',
#  'owners': ['59bc454c16267c000192f683',
#             '67ea90036f7261320122eae5',
#             '67ebcc086f72613201338329'],
#  'package_version': '5.3(0.250001)',
#  'parent': {'class_id': 'mo.MoRef',
#             'link': 'https://intersight.com/api/v1/equipment/Chasses/67ea92456176753301c60ad6',
#             'moid': '67ea92456176753301c60ad6',
#             'object_type': 'equipment.Chassis'},
#  'permission_resources': [{'class_id': 'mo.MoRef',
#                            'link': 'https://intersight.com/api/v1/organization/Organizations/5ddeb51e6972652d30b7fb0a',
#                            'moid': '5ddeb51e6972652d30b7fb0a',
#                            'object_type': 'organization.Organization'},
#                           {'class_id': 'mo.MoRef',
#                            'link': 'https://intersight.com/api/v1/organization/Organizations/67d946ef697265300102cf5a',
#                            'moid': '67d946ef697265300102cf5a',
#                            'object_type': 'organization.Organization'},
#                           {'class_id': 'mo.MoRef',
#                            'link': 'https://intersight.com/api/v1/organization/Organizations/67470bd06972653001275553',
#                            'moid': '67470bd06972653001275553',
#                            'object_type': 'organization.Organization'}],
#  'personality': '',
#  'platform_type': 'IMCBlade',
#  'presence': 'equipped',
#  'registered_device': {'class_id': 'mo.MoRef',
#                        'link': 'https://intersight.com/api/v1/asset/DeviceRegistrations/67ebcc086f72613201338329',
#                        'moid': '67ebcc086f72613201338329',
#                        'object_type': 'asset.DeviceRegistration'},
#  'revision': '',
#  'rn': '',
#  'scaled_mode': '',
#  'serial': 'FCH250671GR',
#  'server_id': 0,
#  'service_profile': '',
#  'shared_scope': '',
#  'slot_id': 6,
#  'source_object_type': 'compute.Blade',
#  'tags': [{'key': 'Intersight.LicenseTier', 'value': 'Advantage'},
#           {'key': 'SITE', 'value': 'LON'}],
#  'topology_scan_status': '',
#  'total_memory': 524288,
#  'tunneled_kvm': False,
#  'user_label': '',
#  'uuid': 'A83FCB2F-2FAC-235D-0003-000000000001',
#  'vendor': 'Cisco Systems Inc'}