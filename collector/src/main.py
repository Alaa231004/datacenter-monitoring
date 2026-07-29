import json
import time
from pathlib import Path
from sender_service import SenderService
from equipment import Equipment
from metric_generator import MetricGenerator

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
            model=item["model"]
        )

        equipments.append(equipment)

    return equipments


def main():

    print("=" * 60)
    print("DATA CENTER MONITORING - COLLECTOR")
    print("=" * 60)

    equipments = load_equipments()

    print(f"\n{len(equipments)} équipements chargés.\n")

    while True:

        print("\n" + "=" * 60)
        print("Nouvelle collecte de données")
        print("=" * 60)

        for equipment in equipments:

            metrics = MetricGenerator.generate(equipment)
            SenderService.send(metrics)
            print(f"\nÉquipement : {metrics['hostname']}")
            print(f"Date : {metrics['timestamp']}")
            print(f"CPU : {metrics['cpu']} %")
            print(f"RAM : {metrics['ram']} %")
            print(f"Disk : {metrics['disk']} %")
            print(f"Temperature : {metrics['temperature']} °C")
            print(f"Power : {metrics['power']} W")
            print(f"Network IN : {metrics['network_in']} Mb/s")
            print(f"Network OUT : {metrics['network_out']} Mb/s")
            print(f"Fan Speed : {metrics['fan_speed']} RPM")
            print(f"Status : {metrics['status']}")

        print("\nProchaine collecte dans 60 secondes...")
        time.sleep(60)


if __name__ == "__main__":
    main()
