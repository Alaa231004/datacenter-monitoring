from equipment import Equipment
from protocols.modbus_client import ModbusClient


equipment = Equipment(
    id=9,
    hostname="AC-001",
    type="Cooling",
    location="Salle Climatisation",
    manufacturer="Schneider",
    model="Cooling Unit",
    protocol="modbus",
    ip="127.0.0.1",
    port=5020,
    slave_id=2
)

metrics = ModbusClient.collect(equipment)

print(metrics)
