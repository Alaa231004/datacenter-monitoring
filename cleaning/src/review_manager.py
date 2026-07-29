def review_metrics(data, anomalies):
    """
    Gère les données nécessitant une revue.
    """

    reviewed = data.copy()
    
    if len(anomalies) == 0:

        reviewed["review_status"] = "APPROVED"
        reviewed["review_comment"] = "Aucune anomalie détectée."

    else:

        reviewed["review_status"] = "PENDING"

        reviewed["review_comment"] = ", ".join(anomalies)

        reviewed["anomaly_count"] = len(anomalies)

    return reviewed
