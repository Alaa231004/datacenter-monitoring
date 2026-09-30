from database import Database


class Repository:

    def __init__(self):
        self.db = Database()

    # ==========================
    # SERVER
    # ==========================

    def get_server_metrics(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM server_metrics
            ORDER BY timestamp DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    # ==========================
    # UPS
    # ==========================

    def get_ups_metrics(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM ups_metrics
            ORDER BY timestamp DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    # ==========================
    # COOLING
    # ==========================

    def get_cooling_metrics(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM cooling_metrics
            ORDER BY timestamp DESC
        """)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    def get_server_statistics(self):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
           SELECT
            COUNT(*) AS total_servers,
            ROUND(AVG(cpu)::numeric,2) AS avg_cpu,
            ROUND(AVG(ram)::numeric,2) AS avg_ram,
            ROUND(AVG(disk)::numeric,2) AS avg_disk,
            ROUND(AVG(temperature)::numeric,2) AS avg_temperature,
            ROUND(AVG(power)::numeric,2) AS avg_power,
            SUM(CASE WHEN risk_level='HIGH' THEN 1 ELSE 0 END) AS critical,
            SUM(CASE WHEN risk_level='MEDIUM' THEN 1 ELSE 0 END) AS warning
          FROM server_metrics
        """)

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return data

    def get_ups_statistics(self):

       conn = self.db.connect()
       cursor = conn.cursor()

       cursor.execute("""
        SELECT
            COUNT(*) AS total_ups,
            ROUND(AVG(battery_level)::numeric,2) AS avg_battery,
            ROUND(AVG(load)::numeric,2) AS avg_load,
            ROUND(AVG(temperature)::numeric,2) AS avg_temperature,
            SUM(CASE WHEN risk_level='HIGH' THEN 1 ELSE 0 END) AS critical,
            SUM(CASE WHEN risk_level='MEDIUM' THEN 1 ELSE 0 END) AS warning
        FROM ups_metrics
       """)

       data = cursor.fetchone()

       cursor.close()
       conn.close()

       return data


    def get_cooling_statistics(self):

       conn = self.db.connect()
       cursor = conn.cursor()

       cursor.execute("""
          SELECT
            COUNT(*) AS total_cooling,
            ROUND(AVG(supply_temperature)::numeric,2) AS avg_supply_temperature,
            ROUND(AVG(return_temperature)::numeric,2) AS avg_return_temperature,
            ROUND(AVG(humidity)::numeric,2) AS avg_humidity,
            ROUND(AVG(power)::numeric,2) AS avg_power,
            SUM(CASE WHEN risk_level='HIGH' THEN 1 ELSE 0 END) AS critical,
            SUM(CASE WHEN risk_level='MEDIUM' THEN 1 ELSE 0 END) AS warning
          FROM cooling_metrics
      """)

       data = cursor.fetchone()

       cursor.close()
       conn.close()

       return data
