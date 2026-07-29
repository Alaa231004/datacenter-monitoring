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
        cleaned[field] = float(cleaned[field])

    return cleaned
