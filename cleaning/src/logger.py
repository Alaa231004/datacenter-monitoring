from datetime import datetime


def log_processing(data, anomalies):
    """
    Affiche les informations de traitement dans le terminal.
    """

    print("\n" + "=" * 60)
    print("        CLEANING SERVICE")
    print("=" * 60)

    print(f"Heure de traitement : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Equipement : {data['hostname']}")
    print(f"Type : {data['type']}")

    print("\n------ METRIQUES ------")

    print(f"CPU : {data['cpu']} %")
    print(f"RAM : {data['ram']} %")
    print(f"Disk : {data['disk']} %")
    print(f"Temperature : {data['temperature']} °C")
    print(f"Power : {data['power']} W")
    print(f"Network IN : {data['network_in']} Mb/s")
    print(f"Network OUT : {data['network_out']} Mb/s")
    print(f"Fan Speed : {data['fan_speed']} RPM")
    print(f"Status : {data['status']}")

    print("\n------ REVIEW ------")

    print(f"Review Status : {data['review_status']}")
    print(f"Comment : {data['review_comment']}")

    if anomalies:
        print("\n------ ANOMALIES DETECTEES ------")
        for anomaly in anomalies:
            print(f"- {anomaly}")
    else:
        print("\nAucune anomalie détectée.")

    print("=" * 60)
