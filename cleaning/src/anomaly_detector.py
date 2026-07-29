from config import *


def detect_anomalies(data):
    """
    Détecte les anomalies métier.
    Retourne une liste d'anomalies détectées.
    """

    anomalies = []

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

    return anomalies
