def normalize_metrics(data):
    """
    Normalise les données afin qu'elles aient toutes
    le même format.
    """

    normalized = data.copy()

    # ==========================
    # Chaînes de caractères
    # ==========================

    normalized["hostname"] = normalized["hostname"].upper()

    normalized["type"] = normalized["type"].upper()

    normalized["status"] = normalized["status"].upper()

    # ==========================
    # Arrondir les valeurs numériques
    # ==========================

    if normalized["type"] == "SERVER":

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

    elif normalized["type"] == "UPS":

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

    elif normalized["type"] == "COOLING":

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

        normalized[field] = round(normalized[field], 2)

    return normalized
