from pymodbus.client.sync import ModbusTcpClient


def test_cooling(slave_id, name):

    client = ModbusTcpClient(
        "127.0.0.1",
        port=5020
    )

    client.connect()

    print("\nConnexion vers :", name)

    result = client.read_holding_registers(
        address=0,
        count=6,
        unit=slave_id
    )

    if result.isError():

        print("Erreur Modbus :", result)

    else:

        print(result)

        print(
            "Registres :",
            result.registers
        )

    client.close()


# AC-001
test_cooling(
    2,
    "AC-001"
)


# AC-002
test_cooling(
    3,
    "AC-002"
)
