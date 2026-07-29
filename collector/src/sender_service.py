import os
import requests

class SenderService:

    URL = os.getenv(
        "CLEANING_URL",
        "http://localhost:5000/metrics"
    )
    @staticmethod
    def send(metrics):

        try:

            response = requests.post(
                SenderService.URL,
                json=metrics,
                timeout=5
            )

            if response.status_code == 200:
                print(f"✅ Données envoyées : {metrics['hostname']}")

            else:
                print(f"❌ Erreur HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:

            print("Impossible de contacter le Cleaning Service")
            print(e)
