from datetime import datetime
from config import *

def validate_metrics(data):
    """
    Vérifie que les données reçues sont valides.
    Retourne (True, "OK") si tout est correct.
    Sinon retourne (False, message d'erreur).
    """

    # ==========================
    # Champs obligatoires
    # ==========================

    required_fields = [
        "equipment_id",
        "hostname",
        "type",
        "timestamp",
        "cpu",
        "ram",
        "disk",
        "temperature",
        "power",
        "network_in",
        "network_out",
        "fan_speed",
        "status"
    ]

    for field in required_fields:
        if field not in data:
            return False, f"Champ manquant : {field}"

    # ==========================
    # Vérification des types
    # ==========================

    numeric_fields = [
        "cpu",
        "ram",
        "disk",
        "temperature",
        "power",
        "network_in",
        "network_out",
        "fan_speed"
    ]

    for field in numeric_fields:
        if not isinstance(data[field], (int, float)):
            return False, f"{field} doit être un nombre."

    if not isinstance(data["hostname"], str):
        return False, "hostname doit être une chaîne."

    if not isinstance(data["type"], str):
        return False, "type doit être une chaîne."

    if not isinstance(data["status"], str):
        return False, "status doit être une chaîne."

    # ==========================
    # Vérification du timestamp
    # ==========================

    try:
        datetime.strptime(
            data["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )
    except ValueError:
        return False, "Format de timestamp invalide."

    # ==========================
    # Vérification des plages
    # ==========================

    if not (MIN_CPU <= data["cpu"] <= MAX_CPU):
        return False, "CPU hors limites."

    if not (MIN_RAM <= data["ram"] <= MAX_RAM):
        return False, "RAM hors limites."

    if not (MIN_DISK <= data["disk"] <= MAX_DISK):
        return False, "Disk hors limites."

    if not (MIN_TEMPERATURE <= data["temperature"] <= MAX_TEMPERATURE):
        return False, "Température hors limites."

    if not (MIN_POWER <= data["power"] <= MAX_POWER):
        return False, "Power hors limites."

    if not (MIN_NETWORK <= data["network_in"] <= MAX_NETWORK):
        return False, "Network IN hors limites."

    if not (MIN_NETWORK <= data["network_out"] <= MAX_NETWORK):
        return False, "Network OUT hors limites."

    if not (MIN_FAN_SPEED <= data["fan_speed"] <= MAX_FAN_SPEED):
        return False, "Fan Speed hors limites."

    # ==========================
    # Vérification du statut
    # ==========================

    if data["status"] not in VALID_STATUS:
        return False, "Status invalide."

    return True, "Validation réussie."
