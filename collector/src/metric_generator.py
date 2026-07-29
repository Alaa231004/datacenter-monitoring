import random
from datetime import datetime


class MetricGenerator:

    @staticmethod
    def generate(equipment):

        cpu = random.randint(10, 95)
        ram = random.randint(20, 90)
        disk = random.randint(30, 95)
        temperature = random.randint(20, 45)
        power = random.randint(250, 850)
        network_in = random.randint(50, 500)
        network_out = random.randint(50, 500)
        fan_speed = random.randint(2500, 5000)

        # Déterminer le statut

        if cpu > 90 or temperature > 42:
            status = "CRITICAL"

        elif cpu > 75 or temperature > 38:
            status = "WARNING"

        else:
            status = "OK"

        return {

            "equipment_id": equipment.id,

            "hostname": equipment.hostname,

            "type": equipment.type,

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "cpu": cpu,

            "ram": ram,

            "disk": disk,

            "temperature": temperature,

            "power": power,

            "network_in": network_in,

            "network_out": network_out,

            "fan_speed": fan_speed,

            "status": status

        }
