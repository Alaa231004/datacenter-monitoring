
from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=5020)

client.connect()

response = client.read_holding_registers(
    address=1,
    count=6,
    unit=2
)

print(response)

if not response.isError():
    print(response.registers)

client.close()
