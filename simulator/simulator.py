import time

from config import UPDATE_INTERVAL
from metrics_generator import (
    initialize_devices,
    update_devices,
    save_state
)

initialize_devices()

save_state()

print("Simulation démarrée")

while True:

    update_devices()

    save_state()

    print("device_state.json mis à jour")

    time.sleep(UPDATE_INTERVAL)
