import json
import time
from pathlib import Path

from sender_service import SenderService
from equipment import Equipment

from protocols.snmp_client import SNMPClient
from protocols.modbus_client import ModbusClient

# Chemin vers le dossier collector
BASE_DIR = Path(__file__).resolve().parent.parent

# Chemin vers le fichier de configuration
CONFIG_FILE = BASE_DIR / "equipements.json"


def load_equipments():
    """Charge les équipements depuis le fichier JSON."""

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    equipments = []

    for item in data:
        equipment = Equipment(
            id=item["id"],
            hostname=item["hostname"],
            type=item["type"],
            location=item["location"],
            manufacturer=item["manufacturer"],
            model=item["model"],
            protocol=item.get("protocol"),
            ip=item.get("ip"),
            port=item.get("port"),
            community=item.get("community"),
            slave_id=item.get("slave_id")
        )

        equipments.append(equipment)

    return equipments


def main():

    print("=" * 60)
    print("DATA CENTER MONITORING - COLLECTOR")
    print("=" * 60)

    equipments = load_equipments()

    print("\nÉquipements chargés :\n")

    for equipment in equipments:
        print(
            equipment.hostname,
            equipment.protocol,
            equipment.ip,
            equipment.port
        )

    print(f"\n{len(equipments)} équipements chargés.\n")

    while True:

        print("\n" + "=" * 60)
        print("Nouvelle collecte de données")
        print("=" * 60)

        for equipment in equipments:

            try:

                if equipment.protocol == "snmp":

                    metrics = SNMPClient.collect(equipment)

                elif equipment.protocol == "modbus":

                    metrics = ModbusClient.collect(equipment)

                else:

                    print(f"Protocole inconnu pour {equipment.hostname}")
                    continue

                SenderService.send(metrics)

                print(f"\nÉquipement : {metrics['hostname']}")
                print(f"Date : {metrics['timestamp']}")

                if equipment.protocol == "snmp":

                    print(f"CPU : {metrics['cpu']} %")
                    print(f"RAM : {metrics['ram']} %")
                    print(f"Disk : {metrics['disk']} %")
                    print(f"Temperature : {metrics['temperature']} °C")
                    print(f"Power : {metrics['power']} W")
                    print(f"Network IN : {metrics['network_in']} Mb/s")
                    print(f"Network OUT : {metrics['network_out']} Mb/s")
                    print(f"Fan Speed : {metrics['fan_speed']} RPM")

                elif equipment.type == "UPS":

                    print(f"Battery : {metrics['battery_level']} %")
                    print(f"Runtime : {metrics['runtime']} min")
                    print(f"Input Voltage : {metrics['input_voltage']} V")
                    print(f"Output Voltage : {metrics['output_voltage']} V")
                    print(f"Frequency : {metrics['frequency']} Hz")
                    print(f"Load : {metrics['load']} %")
                    print(f"Power : {metrics['power']} W")
                    print(f"Temperature : {metrics['temperature']} °C")

                elif equipment.type == "Cooling":

                    print(f"Supply Temperature : {metrics['supply_temperature']} °C")
                    print(f"Return Temperature : {metrics['return_temperature']} °C")
                    print(f"Humidity : {metrics['humidity']} %")
                    print(f"Fan Speed : {metrics['fan_speed']} RPM")
                    print(f"Power : {metrics['power']} W")
                    print(f"Pressure : {metrics['pressure']} Pa")

                    print(f"Status : {metrics['status']}")
            except Exception as e:

                print(f"Erreur avec {equipment.hostname} : {e}")

        print("\nProchaine collecte dans 60 secondes...")
        time.sleep(60)


if __name__ == "__main__":
    main()
