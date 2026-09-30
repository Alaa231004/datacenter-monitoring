from equipment import Equipment
from protocols.snmp_client import SNMPClient

equipment = Equipment(
    id=1,
    hostname="SRV-001",
    type="Server",
    location="Salle A",
    manufacturer="Dell",
    model="R750",
    protocol="snmp",
    ip="127.0.0.1",
    port=11611,
    community="srv001"
)

metrics = SNMPClient.collect(equipment)

print(metrics)
