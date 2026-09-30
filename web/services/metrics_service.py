from services.database import fetch_all, fetch_one


# ============================================================
# SERVERS
# ============================================================

def get_servers(filters=None):

    filters = filters or {}

    query = """
        SELECT
            id,
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
        FROM server_metrics
        WHERE 1=1
    """

    params = []

    if filters.get("hostname"):
        query += " AND hostname ILIKE %s"
        params.append(f"%{filters['hostname']}%")

    if filters.get("status"):
        query += " AND status = %s"
        params.append(filters["status"].upper())

    if filters.get("risk_level"):
        query += " AND risk_level = %s"
        params.append(filters["risk_level"].upper())

    # Filtre par type d'équipement
    if filters.get("equipment_type"):
        equipment_type = filters["equipment_type"].lower()

        if equipment_type not in ("all", "servers", "server"):
            return []

    query += " ORDER BY timestamp DESC"

    return fetch_all(query, params)


# ============================================================
# UPS
# ============================================================

def get_ups(filters=None):

    filters = filters or {}

    query = """
        SELECT
            id,
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
            risk_level,
            collection_source,
            processed_at,
            processed_by,
            review_status,
            review_comment,
            anomaly_count
        FROM ups_metrics
        WHERE 1=1
    """

    params = []

    if filters.get("hostname"):
        query += " AND hostname ILIKE %s"
        params.append(f"%{filters['hostname']}%")

    if filters.get("status"):
        query += " AND status = %s"
        params.append(filters["status"].upper())

    if filters.get("risk_level"):
        query += " AND risk_level = %s"
        params.append(filters["risk_level"].upper())

    # Filtre par type d'équipement
    if filters.get("equipment_type"):
        equipment_type = filters["equipment_type"].lower()

        if equipment_type not in ("all", "ups"):
            return []

    query += " ORDER BY timestamp DESC"

    return fetch_all(query, params)


# ============================================================
# COOLING
# ============================================================

def get_cooling(filters=None):

    filters = filters or {}

    query = """
        SELECT
            id,
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
            risk_level,
            collection_source,
            processed_at,
            processed_by,
            review_status,
            review_comment,
            anomaly_count
        FROM cooling_metrics
        WHERE 1=1
    """

    params = []

    if filters.get("hostname"):
        query += " AND hostname ILIKE %s"
        params.append(f"%{filters['hostname']}%")

    if filters.get("status"):
        query += " AND status = %s"
        params.append(filters["status"].upper())

    if filters.get("risk_level"):
        query += " AND risk_level = %s"
        params.append(filters["risk_level"].upper())

    # Filtre par type d'équipement
    if filters.get("equipment_type"):
        equipment_type = filters["equipment_type"].lower()

        if equipment_type not in ("all", "cooling"):
            return []

    query += " ORDER BY timestamp DESC"

    return fetch_all(query, params)


# ============================================================
# DASHBOARD STATISTICS
# ============================================================
def get_dashboard_statistics():

    # ============================================================
    # DERNIÈRE MESURE DE CHAQUE SERVEUR
    # ============================================================

    server_stats = fetch_one("""
        WITH latest AS (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                status,
                cpu,
                ram,
                temperature,
                power,
                anomaly_count
            FROM server_metrics
            ORDER BY equipment_id, timestamp DESC
        )
        SELECT
            COUNT(*) AS total,

            COUNT(*) FILTER (
                WHERE status = 'OK'
            ) AS ok,

            COUNT(*) FILTER (
                WHERE status = 'WARNING'
            ) AS warning,

            COUNT(*) FILTER (
                WHERE status = 'CRITICAL'
            ) AS critical,

            COALESCE(AVG(cpu), 0) AS avg_cpu,
            COALESCE(AVG(ram), 0) AS avg_ram,
            COALESCE(AVG(temperature), 0) AS avg_temperature,
            COALESCE(AVG(power), 0) AS avg_power,

            COUNT(*) FILTER (
                WHERE anomaly_count > 0
            ) AS anomalies

        FROM latest
    """)


    # ============================================================
    # DERNIÈRE MESURE DE CHAQUE UPS
    # ============================================================

    ups_stats = fetch_one("""
        WITH latest AS (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                status,
                battery_level,
                load,
                temperature,
                power,
                anomaly_count
            FROM ups_metrics
            ORDER BY equipment_id, timestamp DESC
        )
        SELECT
            COUNT(*) AS total,

            COUNT(*) FILTER (
                WHERE status = 'OK'
            ) AS ok,

            COUNT(*) FILTER (
                WHERE status = 'WARNING'
            ) AS warning,

            COUNT(*) FILTER (
                WHERE status = 'CRITICAL'
            ) AS critical,

            COALESCE(AVG(battery_level), 0) AS avg_battery,
            COALESCE(AVG(load), 0) AS avg_load,
            COALESCE(AVG(temperature), 0) AS avg_temperature,
            COALESCE(AVG(power), 0) AS avg_power,

            COUNT(*) FILTER (
                WHERE anomaly_count > 0
            ) AS anomalies

        FROM latest
    """)


    # ============================================================
    # DERNIÈRE MESURE DE CHAQUE COOLING
    # ============================================================

    cooling_stats = fetch_one("""
        WITH latest AS (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                status,
                supply_temperature,
                return_temperature,
                humidity,
                power,
                anomaly_count
            FROM cooling_metrics
            ORDER BY equipment_id, timestamp DESC
        )
        SELECT
            COUNT(*) AS total,

            COUNT(*) FILTER (
                WHERE status = 'OK'
            ) AS ok,

            COUNT(*) FILTER (
                WHERE status = 'WARNING'
            ) AS warning,

            COUNT(*) FILTER (
                WHERE status = 'CRITICAL'
            ) AS critical,

            COALESCE(AVG(supply_temperature), 0)
                AS avg_supply_temperature,

            COALESCE(AVG(return_temperature), 0)
                AS avg_return_temperature,

            COALESCE(AVG(humidity), 0)
                AS avg_humidity,

            COALESCE(AVG(power), 0) AS avg_power,

            COUNT(*) FILTER (
                WHERE anomaly_count > 0
            ) AS anomalies

        FROM latest
    """)


    # ============================================================
    # ANOMALIES = NOMBRE D'ÉQUIPEMENTS AYANT UNE ANOMALIE
    # ============================================================

    anomalies = fetch_one("""
        SELECT
            COUNT(*) AS total_anomalies
        FROM (

            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM server_metrics
            ORDER BY equipment_id, timestamp DESC

        ) AS servers

        WHERE anomaly_count > 0

        UNION ALL

        SELECT
            COUNT(*)
        FROM (

            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM ups_metrics
            ORDER BY equipment_id, timestamp DESC

        ) AS ups

        WHERE anomaly_count > 0

        UNION ALL

        SELECT
            COUNT(*)
        FROM (

            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM cooling_metrics
            ORDER BY equipment_id, timestamp DESC

        ) AS cooling

        WHERE anomaly_count > 0
    """)

    # Le UNION ci-dessus retourne plusieurs lignes.
    # On additionne les résultats.

    anomaly_rows = fetch_all("""
        SELECT COUNT(*) AS count
        FROM (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM server_metrics
            ORDER BY equipment_id, timestamp DESC
        ) s
        WHERE anomaly_count > 0

        UNION ALL

        SELECT COUNT(*) AS count
        FROM (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM ups_metrics
            ORDER BY equipment_id, timestamp DESC
        ) u
        WHERE anomaly_count > 0

        UNION ALL

        SELECT COUNT(*) AS count
        FROM (
            SELECT DISTINCT ON (equipment_id)
                equipment_id,
                anomaly_count
            FROM cooling_metrics
            ORDER BY equipment_id, timestamp DESC
        ) c
        WHERE anomaly_count > 0
    """)

    total_anomalies = sum(
        int(row["count"] or 0)
        for row in anomaly_rows
    )


    return {
        "servers": dict(server_stats),
        "ups": dict(ups_stats),
        "cooling": dict(cooling_stats),
        "total_anomalies": total_anomalies
    }
