from equipment import Equipment
from protocols.modbus_client import ModbusClient


equipment = Equipment(
    id=8,
    hostname="UPS-001",
    type="UPS",
    location="Salle Energie",
    manufacturer="APC",
    model="Smart UPS",
    protocol="modbus",
    ip="127.0.0.1",
    port=5020,
    slave_id=1
)


metrics = ModbusClient.collect(equipment)

print(metrics)
