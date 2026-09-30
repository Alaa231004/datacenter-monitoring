from config import *


def detect_anomalies(data):
    """
    Détecte les anomalies métier.
    Retourne une liste d'anomalies détectées.
    """

    anomalies = []

    # ==========================
    # SERVEUR
    # ==========================

    if data["type"] == "SERVER":

        # CPU
        if data["cpu"] >= CRITICAL_CPU:
            anomalies.append("CPU critique")

        elif data["cpu"] >= WARNING_CPU:
            anomalies.append("CPU élevé")

        # Température
        if data["temperature"] >= CRITICAL_TEMPERATURE:
            anomalies.append("Température critique")

        elif data["temperature"] >= WARNING_TEMPERATURE:
            anomalies.append("Température élevée")

        # RAM
        if data["ram"] >= 95:
            anomalies.append("RAM presque saturée")

        # Disque
        if data["disk"] >= 90:
            anomalies.append("Disque presque plein")

        # Puissance
        if data["power"] > MAX_POWER:
            anomalies.append("Consommation électrique anormale")

        # Ventilateur
        if data["fan_speed"] < MIN_FAN_SPEED:
            anomalies.append("Vitesse du ventilateur anormale")

    # ==========================
    # UPS
    # ==========================

    elif data["type"] == "UPS":

        if data["battery_level"] <= 20:
            anomalies.append("Batterie critique")

        elif data["battery_level"] <= 40:
            anomalies.append("Batterie faible")

        if data["temperature"] >= 40:
            anomalies.append("Température UPS élevée")

        if data["load"] >= 90:
            anomalies.append("Charge UPS élevée")

    # ==========================
    # COOLING
    # ==========================

    elif data["type"] == "COOLING":

        if data["supply_temperature"] >= 24:
            anomalies.append("Température soufflage élevée")

        if data["return_temperature"] >= 32:
            anomalies.append("Température retour élevée")

        if data["humidity"] < 40:
            anomalies.append("Humidité faible")

        elif data["humidity"] > 55:
            anomalies.append("Humidité élevée")

    return anomalies
