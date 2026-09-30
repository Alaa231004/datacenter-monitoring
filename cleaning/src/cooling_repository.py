from database import Database

class CoolingRepository:

    def __init__(self):
        self.db = Database()
    def save(self, data):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cooling_metrics(
                equipment_id,
                hostname,
                timestamp,
                supply_temperature,
                return_temperature,
                humidity,
                fan_speed,
                power,
                pressure,
                status,
                collection_source,
                processed_at,
                processed_by,
                review_status,
                review_comment,
                anomaly_count
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (
            data["equipment_id"],
            data["hostname"],
            data["timestamp"],
            data["supply_temperature"],
            data["return_temperature"],
            data["humidity"],
            data["fan_speed"],
            data["power"],
            data["pressure"],
            data["status"],
            data["collection_source"],
            data["processed_at"],
            data["processed_by"],
            data["review_status"],
            data["review_comment"],
            data.get("anomaly_count",0)
        ))

        conn.commit()
        cursor.close()
        conn.close()
