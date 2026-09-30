from datetime import datetime
from config import COLLECTION_SOURCE, WARNING_CPU, CRITICAL_CPU


def enrich_metrics(data):
    """
    Ajoute des informations utiles aux données.
    """

    enriched = data.copy()


    # ==========================
    # Niveau de risque
    # ==========================

    if enriched["type"] == "SERVER":

        cpu = enriched["cpu"]

        if cpu >= CRITICAL_CPU:
            risk = "HIGH"

        elif cpu >= WARNING_CPU:
            risk = "MEDIUM"

        else:
            risk = "LOW"
    elif enriched["type"] == "UPS":

        if enriched["battery_level"] <= 20:
            risk = "HIGH"

        elif enriched["battery_level"] <= 40:
            risk = "MEDIUM"

        else:
            risk = "LOW"

    elif enriched["type"] == "COOLING":

        if enriched["supply_temperature"] >= 24:
            risk = "HIGH"

        elif enriched["supply_temperature"] >= 21:
            risk = "MEDIUM"

        else:
            risk = "LOW"

    else:

        risk = "LOW"

    enriched["risk_level"] = risk
    # ==========================
    # Source de collecte
    # ==========================

    enriched["collection_source"] = COLLECTION_SOURCE

    # ==========================
    # Date de traitement
    # ==========================

    enriched["processed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================
    # Service ayant traité la donnée
    # ==========================

    enriched["processed_by"] = "cleaning-service"

    return enriched
