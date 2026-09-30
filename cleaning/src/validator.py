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

    if data["type"] == "Server":

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

    elif data["type"] == "UPS":

        required_fields = [
           "equipment_id",
           "hostname",
           "type",
           "timestamp",
           "battery_level",
           "runtime",
           "input_voltage",
           "output_voltage",
           "frequency",
           "load",
           "power",
           "temperature",
           "status"
        ]

    elif data["type"] == "Cooling":

         required_fields = [
            "equipment_id",
            "hostname",
            "type",
            "timestamp",
            "supply_temperature",
            "return_temperature",
            "humidity",
            "fan_speed",
            "power",
            "pressure",
            "status"
         ]

    else:

        return False, "Type d'équipement inconnu."
    for field in required_fields:
        if field not in data:
            return False, f"Champ manquant : {field}"

    # ==========================
    # Vérification des types
    # ==========================

    if data["type"] == "Server":

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

    elif data["type"] == "UPS":

          numeric_fields = [
              "battery_level",
              "runtime",
              "input_voltage",
              "output_voltage",
              "frequency",
              "load",
              "power",
              "temperature"
          ]

    elif data["type"] == "Cooling":

         numeric_fields = [
              "supply_temperature",
              "return_temperature",
              "humidity",
              "fan_speed",
              "power",
              "pressure"
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

    if data["type"] == "Server":

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

    elif data["type"] == "UPS":

        if not (MIN_BATTERY_LEVEL <= data["battery_level"] <= MAX_BATTERY_LEVEL):
            return False, "Battery Level hors limites."

        if not (MIN_RUNTIME <= data["runtime"] <= MAX_RUNTIME):
            return False, "Runtime hors limites."

        if not (MIN_INPUT_VOLTAGE <= data["input_voltage"] <= MAX_INPUT_VOLTAGE):
            return False, "Input Voltage hors limites."

        if not (MIN_OUTPUT_VOLTAGE <= data["output_voltage"] <= MAX_OUTPUT_VOLTAGE):
            return False, "Output Voltage hors limites."

        if not (MIN_FREQUENCY <= data["frequency"] <= MAX_FREQUENCY):
            return False, "Frequency hors limites."

        if not (MIN_LOAD <= data["load"] <= MAX_LOAD):
            return False, "Load hors limites."

        if not (MIN_POWER <= data["power"] <= MAX_POWER):
            return False, "Power hors limites."

        if not (MIN_TEMPERATURE <= data["temperature"] <= MAX_TEMPERATURE):
            return False, "Température hors limites."

    elif data["type"] == "Cooling":

        if not (MIN_SUPPLY_TEMPERATURE <= data["supply_temperature"] <= MAX_SUPPLY_TEMPERATURE):
            return False, "Supply Temperature hors limites."

        if not (MIN_RETURN_TEMPERATURE <= data["return_temperature"] <= MAX_RETURN_TEMPERATURE):
            return False, "Return Temperature hors limites."

        if not (MIN_HUMIDITY <= data["humidity"] <= MAX_HUMIDITY):
            return False, "Humidity hors limites."

        if not (MIN_FAN_SPEED <= data["fan_speed"] <= MAX_FAN_SPEED):
            return False, "Fan Speed hors limites."

        if not (MIN_POWER <= data["power"] <= MAX_POWER):
            return False, "Power hors limites."

        if not (MIN_PRESSURE <= data["pressure"] <= MAX_PRESSURE):
            return False, "Pressure hors limites."
    # ==========================
    # Vérification du statut
    # ==========================

    if data["status"] not in VALID_STATUS:
        return False, "Status invalide."

    return True, "Validation réussie."
