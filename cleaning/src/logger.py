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

    if data["type"] == "SERVER":

          print(f"CPU : {data['cpu']} %")
          print(f"RAM : {data['ram']} %")
          print(f"Disk : {data['disk']} %")
          print(f"Temperature : {data['temperature']} °C")
          print(f"Power : {data['power']} W")
          print(f"Network IN : {data['network_in']} Mb/s")
          print(f"Network OUT : {data['network_out']} Mb/s")
          print(f"Fan Speed : {data['fan_speed']} RPM")
    
    elif data["type"] == "UPS":

          print(f"Battery Level : {data['battery_level']} %")
          print(f"Runtime : {data['runtime']} min")
          print(f"Input Voltage : {data['input_voltage']} V")
          print(f"Output Voltage : {data['output_voltage']} V")
          print(f"Frequency : {data['frequency']} Hz")
          print(f"Load : {data['load']} %")
          print(f"Power : {data['power']} W")
          print(f"Temperature : {data['temperature']} °C")
    
    elif data["type"] == "COOLING":

          print(f"Supply Temperature : {data['supply_temperature']} °C")
          print(f"Return Temperature : {data['return_temperature']} °C")
          print(f"Humidity : {data['humidity']} %")
          print(f"Fan Speed : {data['fan_speed']} RPM")
          print(f"Power : {data['power']} W")
          print(f"Pressure : {data['pressure']} Pa")

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
