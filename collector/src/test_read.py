from pymodbus.client.sync import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=5020)

print("Connexion :", client.connect())

for addr in [0, 1]:
    result = client.read_holding_registers(addr, 1, unit=1)

    if result.isError():
        print(addr, result)
    else:
        print(addr, result.registers)

client.close()
