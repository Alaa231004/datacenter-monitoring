import json
from pathlib import Path
import random

from config import (
    METRIC_RANGES,
    METRIC_VARIATIONS,
    STATUS_VALUES
)

from device_profiles import DEVICE_PROFILES
from device_state import DEVICE_STATE


def initialize_devices():

    with open("../collector/equipements.json", "r") as f:
        equipments = json.load(f)

    for equipment in equipments:

        hostname = equipment["hostname"]
        device_type = equipment["type"]

        DEVICE_STATE[hostname] = {}

        profile = DEVICE_PROFILES[device_type]

        for metric in profile:

            if metric in METRIC_RANGES:

                minimum, maximum = METRIC_RANGES[metric]

                DEVICE_STATE[hostname][metric] = random.randint(
                    minimum,
                    maximum
                )

            else:

                DEVICE_STATE[hostname][metric] = random.choice(
                    STATUS_VALUES[metric]
                )

    return DEVICE_STATE


def update_devices():

    for hostname in DEVICE_STATE:

        for metric in DEVICE_STATE[hostname]:

            # Les métriques d'état comme ON/OFF, UP/DOWN, etc.
            # ne sont pas modifiées ici.
            if metric not in METRIC_RANGES:
                continue

            value = DEVICE_STATE[hostname][metric]

            minimum, maximum = METRIC_RANGES[metric]

            # ==========================================
            # VARIATIONS SPÉCIALES POUR UPS
            # ==========================================

            if hostname == "UPS-001":

                if metric == "temperature":

                    variation = random.randint(-2, 2)

                elif metric == "battery_level":

                    variation = random.randint(-1, 1)

                elif metric == "power":

                    variation = random.randint(-50, 50)

                elif metric == "load":

                    variation = random.randint(-3, 3)

                else:

                    minimum_variation, maximum_variation = \
                        METRIC_VARIATIONS[metric]

                    variation = random.randint(
                        minimum_variation,
                        maximum_variation
                    )

            # ==========================================
            # AUTRES ÉQUIPEMENTS
            # ==========================================

            else:

                minimum_variation, maximum_variation = \
                    METRIC_VARIATIONS[metric]

                variation = random.randint(
                    minimum_variation,
                    maximum_variation
                )

            # ==========================================
            # NOUVELLE VALEUR
            # ==========================================

            new_value = value + variation

            # Respecter la valeur minimale
            if new_value < minimum:
                new_value = minimum

            # Respecter la valeur maximale
            if new_value > maximum:
                new_value = maximum

            DEVICE_STATE[hostname][metric] = new_value

    print("UPS :", DEVICE_STATE["UPS-001"])
    print("AC-001 :", DEVICE_STATE["AC-001"])
    print("AC-002 :", DEVICE_STATE["AC-002"])


def save_state():

    output_file = Path("data/device_state.json")

    with open(output_file, "w") as f:

        json.dump(
            DEVICE_STATE,
            f,
            indent=4
        )
