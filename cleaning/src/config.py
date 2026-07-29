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
MAX_TEMPERATURE = 60

WARNING_TEMPERATURE = 38
CRITICAL_TEMPERATURE = 42

# ==========================
# POWER (Watts)
# ==========================

MIN_POWER = 100
MAX_POWER = 900

# ==========================
# NETWORK (Mb/s)
# ==========================

MIN_NETWORK = 0
MAX_NETWORK = 1000

# ==========================
# FAN SPEED (RPM)
# ==========================

MIN_FAN_SPEED = 1000
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
