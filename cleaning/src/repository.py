from database import Database


class Repository:

    def __init__(self):
        self.db = Database()

    def save_metrics(self, data):

        connection = self.db.connect()

        if connection is None:
            return False

        try:

            cursor = connection.cursor()

            query = """
            INSERT INTO metrics (
                equipment_id,
                hostname,
                type,
                timestamp,
                cpu,
                ram,
                disk,
                temperature,
                power,
                network_in,
                network_out,
                fan_speed,
                status,
                risk_level,
                collection_source,
                processed_at,
                processed_by,
                review_status,
                review_comment,
                anomaly_count
            )
            VALUES (
                %(equipment_id)s,
                %(hostname)s,
                %(type)s,
                %(timestamp)s,
                %(cpu)s,
                %(ram)s,
                %(disk)s,
                %(temperature)s,
                %(power)s,
                %(network_in)s,
                %(network_out)s,
                %(fan_speed)s,
                %(status)s,
                %(risk_level)s,
                %(collection_source)s,
                %(processed_at)s,
                %(processed_by)s,
                %(review_status)s,
                %(review_comment)s,
                %(anomaly_count)s
            );
            """

            cursor.execute(query, data)

            connection.commit()

            cursor.close()

            self.db.close(connection)

            print("Donnée enregistrée dans PostgreSQL.")

            return True

        except Exception as e:

            print("Erreur insertion PostgreSQL :")
            print(e)

            connection.rollback()

            self.db.close(connection)

            return False

    def get_all(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []


    def get_critical_metrics(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE status = 'CRITICAL'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []

    def get_warning_metrics(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE status = 'WARNING'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []

    def get_UPS(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE Type = 'UPS'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []



    def get_routeur(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE type = 'ROUTER'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []


    def get_ok_metrics(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE status = 'OK'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []

    def get_servers(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE type = 'SERVER'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []

    def get_switchs(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE type = 'SWITCH'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []


    def get_cooling(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE type = 'COOLING'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []



    def get_firewall(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE type = 'FIREWALL'
            ORDER BY id DESC;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []


    def get_last_50_metrics(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            ORDER BY id DESC
            LIMIT 50;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []



    def get_metrics_by_equipment(self, hostname):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
            SELECT *
            FROM metrics
            WHERE hostname = %s
            ORDER BY timestamp DESC;
            """

            cursor.execute(query, (hostname,))

            rows = cursor.fetchall()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)
            self.db.close(connection)

            return []

    def get_dashboard_statistics(self):

        connection = self.db.connect()

        if connection is None:
            return {}

        try:

            cursor = connection.cursor()

            statistics = {}

            # Nombre total d'équipements
            cursor.execute("""
                SELECT COUNT(DISTINCT equipment_id)
                FROM metrics;
            """)

            result = cursor.fetchone()
            statistics["total_equipments"] = result["count"]

            # Nombre par type
            cursor.execute("""
                SELECT type, COUNT(DISTINCT equipment_id) AS count
                FROM metrics
                GROUP BY type;
            """)
            type_rows = cursor.fetchall()

            statistics["by_type"] = {}

            for row in type_rows:
                statistics["by_type"][row["type"]] = row["count"]

            # Nombre par statut
            cursor.execute("""
                SELECT status, COUNT(*) AS count
                FROM metrics
                GROUP BY status;
            """)

            status_rows = cursor.fetchall()

            statistics["by_status"] = {}

            for row in status_rows:
                statistics["by_status"][row["status"]] = row["count"]

            # Moyennes
            cursor.execute("""
                SELECT
                    AVG(cpu) AS avg_cpu,
                    AVG(ram) AS avg_ram,
                    AVG(temperature) AS avg_temperature,
                    AVG(power) AS avg_power
                FROM metrics;
            """)

            averages = cursor.fetchone()

            statistics["averages"] = {
                "cpu": round(float(averages["avg_cpu"]), 2),
                "ram": round(float(averages["avg_ram"]), 2),
                "temperature": round(float(averages["avg_temperature"]), 2),
                "power": round(float(averages["avg_power"]), 2)
            }

            cursor.close()
            self.db.close(connection)

            return statistics

        except Exception as e:

            import traceback

            print("========= ERREUR COMPLETE =========")
            traceback.print_exc()

            self.db.close(connection)

            return {}

    def get_cpu_history(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                date_trunc('minute', timestamp) AS timestamp,
                ROUND(AVG(cpu)::numeric, 2) AS cpu
            FROM metrics
            GROUP BY date_trunc('minute', timestamp)
            ORDER BY timestamp DESC
            LIMIT 60;
            """

            cursor.execute(query)

            rows = cursor.fetchall()
           
            rows.reverse()
            cursor.close()

            self.db.close(connection)
            print(rows)
            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []


    def get_temperature_history(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                date_trunc('minute', timestamp) AS timestamp,
                ROUND(AVG(temperature)::numeric, 2) AS temperature
            FROM metrics
            GROUP BY date_trunc('minute', timestamp)
            ORDER BY timestamp DESC
            LIMIT 60;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            rows.reverse()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []


    def get_power_history(self):

        connection = self.db.connect()

        if connection is None:
            return []

        try:

            cursor = connection.cursor()

            query = """
                SELECT
                date_trunc('minute', timestamp) AS timestamp,
                ROUND(AVG(power)::numeric, 2) AS power
            FROM metrics
            GROUP BY date_trunc('minute', timestamp)
            ORDER BY timestamp DESC
            LIMIT 60;
            """

            cursor.execute(query)

            rows = cursor.fetchall()

            rows.reverse()

            cursor.close()

            self.db.close(connection)

            return rows

        except Exception as e:

            print("Erreur lecture PostgreSQL :")
            print(e)

            self.db.close(connection)

            return []
