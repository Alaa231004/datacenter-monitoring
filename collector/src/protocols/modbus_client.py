from pymodbus.client.sync import ModbusTcpClient
from datetime import datetime


class ModbusClient:

    @staticmethod
    def collect(equipment):

        client = ModbusTcpClient(
            equipment.ip,
            port=equipment.port
        )

        try:

            connected = client.connect()

            if not connected:
                raise Exception("Impossible de se connecter au serveur Modbus")

            print(
                "Connexion Modbus vers:",
                equipment.ip,
                equipment.port,
                "slave:",
                equipment.slave_id
            )
            # Lecture des registres selon le type d'équipement

            if equipment.type == "UPS":

                result = client.read_holding_registers(
                    address=0,
                    count=8,
                    unit=equipment.slave_id
                )
                print(result)

            elif equipment.type == "Cooling":

                result = client.read_holding_registers(
                    address=0,
                    count=6,
                    unit=equipment.slave_id
                )

            elif equipment.type == "PDU":

                result = client.read_holding_registers(
                    address=0,
                    count=6,
                    unit=equipment.slave_id
                )

            else:

                raise Exception(
                    f"Type Modbus inconnu : {equipment.type}"
                )

            if not result.isError():
                print(result.registers)
            if result.isError():
                print("Réponse Modbus :", result)
                raise Exception("Erreur lecture Modbus")

            registers = result.registers
            # ---------------- UPS ----------------

            if equipment.type == "UPS":

                battery_level = registers[0]
                runtime = registers[1]
                input_voltage = registers[2]
                output_voltage = registers[3]
                frequency = registers[4]
                load = registers[5]
                power = registers[6]
                temperature = registers[7]

                if temperature > 42 or battery_level < 20:
                       status = "CRITICAL"

                elif temperature > 38 or battery_level < 40:
                       status = "WARNING"

                else:
                       status = "OK"
                metrics = {

                    "equipment_id": equipment.id,
                    "hostname": equipment.hostname,
                    "type": equipment.type,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                    "battery_level": battery_level,
                    "runtime": runtime,
                    "input_voltage": input_voltage,
                    "output_voltage": output_voltage,
                    "frequency": frequency,
                    "load": load,
                    "power": power,
                    "temperature": temperature,

                    "status": status
                }

            # ---------------- Cooling ----------------

            elif equipment.type == "Cooling":

                  supply_temperature = registers[0]
                  return_temperature = registers[1]
                  humidity = registers[2]
                  fan_speed = registers[3]
                  power = registers[4]
                  pressure = registers[5]

                  if return_temperature > 35 or supply_temperature > 25:
                          status = "CRITICAL"

                  elif return_temperature > 30 or supply_temperature > 22:
                          status = "WARNING"

                  else:
                          status = "OK"
                  metrics = {
                
                      "equipment_id": equipment.id,
                      "hostname": equipment.hostname,
                      "type": equipment.type,
                      "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                      "supply_temperature": supply_temperature,
                      "return_temperature": return_temperature,
                      "humidity": humidity,
                      "fan_speed": fan_speed,
                      "power": power,
                      "pressure": pressure,

                      "status": status

                  }

            # ---------------- PDU ----------------

            elif equipment.type == "PDU":

                metrics = {

                    "equipment_id": equipment.id,
                    "hostname": equipment.hostname,
                    "type": equipment.type,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

            return metrics

        finally:
            client.close()
