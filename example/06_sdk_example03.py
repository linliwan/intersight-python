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
fabric = intersight.apis.FabricApi(api_client=client)
network = intersight.apis.NetworkApi(api_client=client)
equipment = intersight.apis.EquipmentApi(api_client=client)
port = intersight.apis.PortApi(api_client=client)
ether = intersight.apis.EtherApi(api_client=client)

fi_moid = fabric.get_fabric_switch_cluster_profile_list(**{'filter': "Name eq 'LON-AI1-FI1'"}).results[0].cluster_assignments[0].network_element.moid
fi = network.get_network_element_by_moid(moid=fi_moid)
fi_cards = fi.cards

# used to store fi peer information
peer_moid_list = []
for fi_card in fi_cards:
    port_groups = equipment.get_equipment_switch_card_by_moid(moid=fi_card.moid).port_groups
    for pg in port_groups:
        eth_ports = port.get_port_group_by_moid(moid=pg.moid).ethernet_ports
        for ep in eth_ports:
            peer_int = ether.get_ether_physical_port_by_moid(moid=ep.moid).peer_interface
            if peer_int:
                peer_moid_list.append(peer_int.moid)

print(f"================== {fi.switch_type} {fi.model} {fi.serial} neighbor list:\n{peer_moid_list}")

# used to store chasses information
chassis_moid_set = set()
for moid in peer_moid_list:
    ancestors = ether.get_ether_network_port_by_moid(moid).ancestors
    for ancestor in ancestors:
        if ancestor.object_type == "equipment.Chassis":
            chassis_moid_set.add(ancestor.moid)
print(f"================== Chassis list:\n{chassis_moid_set}")

# store all attached blades information
results = []
for moid in chassis_moid_set:
    chassis = equipment.get_equipment_chassis_by_moid(moid)
    blades = chassis.blades
    for blade in blades:
        results.append((chassis, compute.get_compute_blade_by_moid(blade.moid)))
print("\n================== Results:")
for item in results:
    print(f"Server: {item[1].model} | Serial: {item[1].serial} | Chassis Model: {item[0].model} | Chassis Serial: {item[0].serial}")


# ================== FabricInterconnect UCS-FI-6536 FDO27490P6K neighbor list:
# ['67ea924b6176753301c6143a', '67ea92626176753301c63d4d', '67ea92696176753301c6487e', '67ea92616176753301c63c4b', '67ea92496176753301c60f8f', '67ea924a6176753301c612b7', '67ea924d6176753301c6184f', '67ea92586176753301c62a9b']
# ================== Chassis list:
# {'67ea92456176753301c60ad6'}

# ================== Results:
# Server: UCSX-210C-M7 | Serial: FCH27487545 | Chassis Model: UCSX-9508 | Chassis Serial: FOX2747PKPT
# Server: UCSX-210C-M7 | Serial: FCH274875AV | Chassis Model: UCSX-9508 | Chassis Serial: FOX2747PKPT
# Server: UCSX-210C-M6 | Serial: FCH250671PP | Chassis Model: UCSX-9508 | Chassis Serial: FOX2747PKPT
# Server: UCSX-210C-M6 | Serial: FCH250671GR | Chassis Model: UCSX-9508 | Chassis Serial: FOX2747PKPT
# Server: UCSX-210C-M6 | Serial: FCH264477D7 | Chassis Model: UCSX-9508 | Chassis Serial: FOX2747PKPT