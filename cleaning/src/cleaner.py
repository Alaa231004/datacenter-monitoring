def clean_metrics(data):
    """
    Nettoyage des données.
    Corrige uniquement les problèmes de format.
    """

    cleaned = data.copy()

    # ==========================
    # Nettoyage des chaînes
    # ==========================

    cleaned["hostname"] = cleaned["hostname"].strip()
    cleaned["type"] = cleaned["type"].strip()
    cleaned["status"] = cleaned["status"].strip()



    # ==========================
    # Conversion des valeurs numériques
    # ==========================

    if cleaned["type"] == "Server":

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
    elif cleaned["type"] == "UPS":

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

    elif cleaned["type"] == "Cooling":

        numeric_fields = [
            "supply_temperature",
            "return_temperature",
            "humidity",
            "fan_speed",
            "power",
            "pressure"
        ]

    else:

        numeric_fields = []

    for field in numeric_fields:

        cleaned[field] = float(cleaned[field])

    return cleaned
