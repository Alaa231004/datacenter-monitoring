from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartTcpServer
import json
from pathlib import Path
import threading
import time
import random
import os
def load_device_state():
    path = os.getenv("DEVICE_STATE_PATH", "/shared/device_state.json")
    with open(Path(path), "r") as f:
        return json.load(f)



devices = load_device_state()

ups = devices["UPS-001"]
ac1 = devices["AC-001"]
ac2 = devices["AC-002"]


slaves = {
    1: ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(
            0,
            [
                ups["battery_level"],
                ups["runtime"],
                ups["input_voltage"],
                ups["output_voltage"],
                ups["frequency"],
                ups["load"],
                ups["power"],
                ups["temperature"]
            ]
        )
    ),

    2: ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 20)
    ),

    3: ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 20)
    )
}


print("Slaves disponibles :", list(slaves.keys()))

context = ModbusServerContext(
    slaves=slaves,
    single=False
)


def update_registers():

    battery = ups["battery_level"]
    temperature = ups["temperature"]

    while True:

        # UPS
        battery += random.randint(-1, 1)
        battery = max(80, min(100, battery))

        temperature += random.randint(-1, 1)
        temperature = max(20, min(50, temperature))

        runtime = random.randint(20, 90)
        input_voltage = random.randint(220, 240)
        output_voltage = random.randint(220, 240)
        frequency = random.randint(49, 51)
        load = random.randint(10, 90)
        power = random.randint(200, 900)

        context[1].setValues(
            3,
            0,
            [
                battery,
                runtime,
                input_voltage,
                output_voltage,
                frequency,
                load,
                power,
                temperature
            ]
        )

        # Cooling 1
        context[2].setValues(
            3,
            0,
            [
                random.randint(15, 25),
                random.randint(20, 35),
                random.randint(35, 60),
                random.randint(2000, 5000),
                random.randint(200, 900),
                random.randint(950, 1050)
            ]
        )

        # Cooling 2
        context[3].setValues(
            3,
            0,
            [
                random.randint(15, 25),
                random.randint(20, 35),
                random.randint(35, 60),
                random.randint(2000, 5000),
                random.randint(200, 900),
                random.randint(950, 1050)
            ]
        )

        print(
            f"UPS -> Battery: {battery}% | "
            f"Temperature: {temperature}°C | "
            f"Power: {power}W"
        )

        time.sleep(5)


if __name__ == "__main__":

    print("Démarrage serveur Modbus simulé sur 127.0.0.1:5020")

    threading.Thread(
        target=update_registers,
        daemon=True
    ).start()

    StartTcpServer(
        context=context,
        address=("0.0.0.0", 5020)
    )
