import json
from pathlib import Path


SNMP_FILES = {

    "SRV-001": "../snmp-sim/data/srv001.snmprec",
    "SRV-002": "../snmp-sim/data/srv002.snmprec",
    "SRV-003": "../snmp-sim/data/srv003.snmprec",

    "SW-001": "../snmp-sim/data/sw001.snmprec",
    "SW-002": "../snmp-sim/data/sw002.snmprec",

    "RTR-001": "../snmp-sim/data/rtr001.snmprec",

    "FW-001": "../snmp-sim/data/fw001.snmprec"

}
SERVER_OIDS = {
    "cpu": "1.3.6.1.4.1.2021.11.9.0",
    "ram": "1.3.6.1.4.1.2021.4.6.0",
    "cpu_temperature": "1.3.6.1.4.1.2021.13.16.2.1.3.1",
    "disk": "1.3.6.1.4.1.2021.9.1.0",
    "power": "1.3.6.1.4.1.2021.10.1.0",
    "network_in": "1.3.6.1.4.1.2021.11.1.0",
    "network_out": "1.3.6.1.4.1.2021.11.2.0",
    "fan_speed": "1.3.6.1.4.1.2021.12.1.0"
}
SWITCH_OIDS = {

    "cpu": "1.3.6.1.4.1.2021.11.9.0",
    "memory": "1.3.6.1.4.1.2021.4.6.0",
    "temperature": "1.3.6.1.4.1.2021.13.16.2.1.3.1",

    "network_in": "1.3.6.1.4.1.2021.11.1.0",
    "network_out": "1.3.6.1.4.1.2021.11.2.0",

    "active_ports": "1.3.6.1.4.1.2021.20.1.0",
    "interface_errors": "1.3.6.1.4.1.2021.20.2.0",

    "power": "1.3.6.1.4.1.2021.10.1.0"
}

ROUTER_OIDS = {

    "cpu": "1.3.6.1.4.1.2021.11.9.0",

    "memory": "1.3.6.1.4.1.2021.4.6.0",

    "network_in": "1.3.6.1.4.1.2021.11.1.0",

    "network_out": "1.3.6.1.4.1.2021.11.2.0",

    "active_routes": "1.3.6.1.4.1.2021.30.1.0",

    "temperature": "1.3.6.1.4.1.2021.13.16.2.1.3.1"

}

FIREWALL_OIDS = {

    "cpu": "1.3.6.1.4.1.2021.11.9.0",

    "memory": "1.3.6.1.4.1.2021.4.6.0",

    "active_sessions": "1.3.6.1.4.1.2021.40.1.0",

    "network_throughput": "1.3.6.1.4.1.2021.40.2.0",

    "connections": "1.3.6.1.4.1.2021.40.3.0",

    "temperature": "1.3.6.1.4.1.2021.13.16.2.1.3.1"

}
def load_device_state():

    with open("data/device_state.json", "r") as f:
        return json.load(f)



def update_server(hostname, device):
    output = Path(SNMP_FILES[hostname])

    lines = [

        f"1.3.6.1.2.1.1.1.0|4|Dell PowerEdge R750 - {hostname}\n",
        f"{SERVER_OIDS['cpu']}|2|{device['cpu']}\n",

        f"1.3.6.1.4.1.2021.4.6.0|2|{device['ram']}\n",

        f"1.3.6.1.4.1.2021.13.16.2.1.3.1|2|{device['cpu_temperature']}\n",

        f"{SERVER_OIDS['disk']}|2|{device['disk']}\n",

        f"{SERVER_OIDS['power']}|2|{device['power']}\n",

        f"{SERVER_OIDS['network_in']}|2|{device['network_in']}\n",

        f"{SERVER_OIDS['network_out']}|2|{device['network_out']}\n",

        f"{SERVER_OIDS['fan_speed']}|2|{device['fan_speed']}\n"

    ]

    with open(output, "w") as f:
        f.writelines(lines)


def update_switch(hostname, device):

    output = Path(SNMP_FILES[hostname])

    lines = [

        f"1.3.6.1.2.1.1.1.0|4|Cisco Catalyst 9300 - {hostname}\n",

        f"{SWITCH_OIDS['cpu']}|2|{device['cpu']}\n",

        f"{SWITCH_OIDS['memory']}|2|{device['memory']}\n",

        f"{SWITCH_OIDS['temperature']}|2|{device['temperature']}\n",

        f"{SWITCH_OIDS['network_in']}|2|{device['network_in']}\n",

        f"{SWITCH_OIDS['network_out']}|2|{device['network_out']}\n",

        f"{SWITCH_OIDS['active_ports']}|2|{device['active_ports']}\n",

        f"{SWITCH_OIDS['interface_errors']}|2|{device['interface_errors']}\n",

        f"{SWITCH_OIDS['power']}|2|{device['power']}\n"

    ]

    with open(output, "w") as f:
        f.writelines(lines)

def update_router(hostname, device):

    output = Path(SNMP_FILES[hostname])

    lines = [

        f"1.3.6.1.2.1.1.1.0|4|Cisco ISR 4451 - {hostname}\n",

        f"{ROUTER_OIDS['cpu']}|2|{device['cpu']}\n",

        f"{ROUTER_OIDS['memory']}|2|{device['memory']}\n",

        f"{ROUTER_OIDS['network_in']}|2|{device['network_in']}\n",

        f"{ROUTER_OIDS['network_out']}|2|{device['network_out']}\n",

        f"{ROUTER_OIDS['active_routes']}|2|{device['active_routes']}\n",

        f"{ROUTER_OIDS['temperature']}|2|{device['temperature']}\n"

    ]

    with open(output, "w") as f:
        f.writelines(lines)
def update_firewall(hostname, device):

    output = Path(SNMP_FILES[hostname])

    lines = [

        f"1.3.6.1.2.1.1.1.0|4|Fortinet FortiGate - {hostname}\n",

        f"{FIREWALL_OIDS['cpu']}|2|{device['cpu']}\n",

        f"{FIREWALL_OIDS['memory']}|2|{device['memory']}\n",

        f"{FIREWALL_OIDS['active_sessions']}|2|{device['active_sessions']}\n",

        f"{FIREWALL_OIDS['network_throughput']}|2|{device['network_throughput']}\n",

        f"{FIREWALL_OIDS['connections']}|2|{device['connections']}\n",

        f"{FIREWALL_OIDS['temperature']}|2|{device['temperature']}\n"

    ]

    with open(output, "w") as f:
        f.writelines(lines)

if __name__ == "__main__":


    devices = load_device_state()

    for hostname, metrics in devices.items():

        if hostname.startswith("SRV"):

            update_server(hostname, metrics)
    
        elif hostname.startswith("SW"):

            update_switch(hostname, metrics)
    
        elif hostname.startswith("RTR"):

            update_router(hostname, metrics)

        elif hostname.startswith("FW"):

            update_firewall(hostname, metrics)

    print("Tous les serveurs ont été mis à jour.")
 
