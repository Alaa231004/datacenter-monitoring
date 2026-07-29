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
        normalized[field] = round(normalized[field], 2)

    return normalized
