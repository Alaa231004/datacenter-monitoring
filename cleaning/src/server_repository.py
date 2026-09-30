from database import Database

class ServerRepository:

    def __init__(self):
        self.db = Database()
    def save(self, data):

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO server_metrics(
                equipment_id,
                hostname,
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
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (
            data["equipment_id"],
            data["hostname"],
            data["timestamp"],
            data["cpu"],
            data["ram"],
            data["disk"],
            data["temperature"],
            data["power"],
            data["network_in"],
            data["network_out"],
            data["fan_speed"],
            data["status"],
            data["risk_level"],
            data["collection_source"],
            data["processed_at"],
            data["processed_by"],
            data["review_status"],
            data["review_comment"],
            data.get("anomaly_count", 0)       
           ))

        conn.commit()
        cursor.close()
        conn.close()
