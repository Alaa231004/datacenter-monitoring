from database import Database

class UPSRepository:

    def __init__(self):
        self.db = Database()
    def save(self, data):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ups_metrics(
                equipment_id,
                hostname,
                timestamp,
                battery_level,
                runtime,
                input_voltage,
                output_voltage,
                frequency,
                load,
                power,
                temperature,
                status,
                collection_source,
                processed_at,
                processed_by,
                review_status,
                review_comment,
                anomaly_count
            )
            VALUES (
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (
            data["equipment_id"],
            data["hostname"],
            data["timestamp"],
            data["battery_level"],
            data["runtime"],
            data["input_voltage"],
            data["output_voltage"],
            data["frequency"],
            data["load"],
            data["power"],
            data["temperature"],
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
