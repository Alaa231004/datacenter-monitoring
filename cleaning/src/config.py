# ==========================
# CPU
# ==========================

MIN_CPU = 0
MAX_CPU = 100
WARNING_CPU = 80
CRITICAL_CPU = 90

# ==========================
# RAM
# ==========================

MIN_RAM = 0
MAX_RAM = 100

# ==========================
# DISK
# ==========================

MIN_DISK = 0
MAX_DISK = 100

# ==========================
# TEMPERATURE (°C)
# ==========================

MIN_TEMPERATURE = 15
MAX_TEMPERATURE = 90

WARNING_TEMPERATURE = 70
CRITICAL_TEMPERATURE = 80

# ==========================
# POWER (Watts)
# ==========================

MIN_POWER = 0
MAX_POWER = 1000

# ==========================
# NETWORK (Mb/s)
# ==========================

MIN_NETWORK = 0
MAX_NETWORK = 1000

# ==========================
# FAN SPEED (RPM)
# ==========================

MIN_FAN_SPEED = 0
MAX_FAN_SPEED = 6000

# ==========================
# STATUS AUTORISÉS
# ==========================

VALID_STATUS = [
    "OK",
    "WARNING",
    "CRITICAL"
]

# ==========================
# COLLECTION
# ==========================

COLLECTION_SOURCE = "collector-1"
# ==========================
# UPS
# ==========================

MIN_BATTERY_LEVEL = 0
MAX_BATTERY_LEVEL = 100

MIN_RUNTIME = 0
MAX_RUNTIME = 120

MIN_INPUT_VOLTAGE = 200
MAX_INPUT_VOLTAGE = 250

MIN_OUTPUT_VOLTAGE = 200
MAX_OUTPUT_VOLTAGE = 250

MIN_FREQUENCY = 45
MAX_FREQUENCY = 55

MIN_LOAD = 0
MAX_LOAD = 100

# ==========================
# COOLING
# ==========================

MIN_SUPPLY_TEMPERATURE = 10
MAX_SUPPLY_TEMPERATURE = 30

MIN_RETURN_TEMPERATURE = 15
MAX_RETURN_TEMPERATURE = 45

MIN_HUMIDITY = 0
MAX_HUMIDITY = 100

MIN_PRESSURE = 900
MAX_PRESSURE = 1100
