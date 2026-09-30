UPDATE_INTERVAL = 60

# ==========================================================
# PLAGES DE VALEURS DES MÉTRIQUES
# ==========================================================

METRIC_RANGES = {

    # -----------------------
    # Serveurs
    # -----------------------
    "cpu": (10, 95),
    "ram": (20, 95),
    "disk": (10, 90),

    "cpu_temperature": (35, 85),
    "motherboard_temperature": (30, 60),

    "fan_speed": (2000, 5000),

    "power": (200, 900),

    "network_in": (10, 1000),
    "network_out": (10, 1000),

    "processes": (80, 350),

    # -----------------------
    # Switch / Routeur / Firewall
    # -----------------------
    "memory": (20, 90),

    "temperature": (20, 50),

    "active_ports": (5, 48),
    "interface_errors": (0, 10),

    "active_routes": (50, 300),

    "active_sessions": (100, 10000),
    "connections": (50, 5000),

    "network_throughput": (10, 1000),

    # -----------------------
    # UPS
    # -----------------------
    "battery_level": (80, 100),
    "runtime": (20, 90),

    "input_voltage": (220, 240),
    "output_voltage": (220, 240),

    "frequency": (49, 51),

    "load": (10, 90),

    # -----------------------
    # Cooling
    # -----------------------
    "supply_temperature": (15, 25),

    "return_temperature": (20, 35),

    "humidity": (35, 60),

    "pressure": (950, 1050),

    # -----------------------
    # PDU
    # -----------------------
    "current": (5, 80),

    "voltage": (220, 240),

    "energy": (1000, 50000)
}


# ==========================================================
# VARIATION À CHAQUE COLLECTE
# ==========================================================

METRIC_VARIATIONS = {

    # Serveurs
    "cpu": (-10, 10),
    "ram": (-3, 3),
    "disk": (-2, 2),

    "cpu_temperature": (-2, 2),
    "motherboard_temperature": (-1, 1),

    "fan_speed": (-100, 100),

    "power": (-20, 20),

    "network_in": (-100, 100),
    "network_out": (-100, 100),

    "processes": (-5, 5),

    # Switch / Routeur / Firewall
    "memory": (-3, 3),

    "temperature": (-1, 1),

    "active_ports": (-1, 1),
    "interface_errors": (0, 1),

    "active_routes": (-2, 2),

    "active_sessions": (-100, 100),
    "connections": (-50, 50),

    "network_throughput": (-100, 100),

    # UPS
    "battery_level": (-1, 1),
    "runtime": (-1, 1),

    "input_voltage": (-2, 2),
    "output_voltage": (-2, 2),

    "frequency": (-1, 1),

    "load": (-2, 2),
    "power": (-50, 50),
    "temperature": (-2, 2),
    # Cooling
    "supply_temperature": (-1, 1),

    "return_temperature": (-1, 1),

    "humidity": (-2, 2),

    "pressure": (-2, 2),

    # PDU
    "current": (-2, 2),

    "voltage": (-2, 2),

    "energy": (5, 30)
}


# ==========================================================
# MÉTRIQUES DE TYPE ÉTAT
# ==========================================================

STATUS_VALUES = {

    "power_supply_status": [
        "OK",
        "FAILED"
    ],

    "battery_status": [
        "NORMAL",
        "LOW",
        "CRITICAL"
    ],

    "port_status": [
        "UP",
        "DOWN"
    ],

    "interface_status": [
        "UP",
        "DOWN"
    ],

    "compressor_status": [
        "ON",
        "OFF"
    ]
}

