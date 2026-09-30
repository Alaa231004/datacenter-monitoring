from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient(
    "127.0.0.1",
    port=5020
)

print("Connexion :", client.connect())

result = client.read_holding_registers(
    address=1,
    count=3,
    unit=1
)

print(result)

if not result.isError():
    print(result.registers)

client.close()
