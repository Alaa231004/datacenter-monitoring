#!/usr/bin/env python3

import random
import sys

# OID des métriques serveur
CPU_OID = "1.3.6.1.4.1.2021.11.9.0"
RAM_OID = "1.3.6.1.4.1.2021.4.6.0"
TEMP_OID = "1.3.6.1.4.1.2021.13.16.2.1.3.1"
DISK_OID = "1.3.6.1.4.1.2021.9.1.0"
POWER_OID = "1.3.6.1.4.1.2021.10.1.0"
NETWORK_IN_OID = "1.3.6.1.4.1.2021.11.1.0"
NETWORK_OUT_OID = "1.3.6.1.4.1.2021.11.2.0"
FAN_SPEED_OID = "1.3.6.1.4.1.2021.12.1.0"


def generate_metric(oid):

    if oid == CPU_OID:
        return random.randint(10, 95)

    elif oid == RAM_OID:
        return random.randint(20, 90)

    elif oid == TEMP_OID:
        return random.randint(20, 45)

    elif oid == DISK_OID:
        return random.randint(30, 95)

    elif oid == POWER_OID:
        return random.randint(250, 850)

    elif oid == NETWORK_IN_OID:
        return random.randint(50, 500)

    elif oid == NETWORK_OUT_OID:
        return random.randint(50, 500)

    elif oid == FAN_SPEED_OID:
        return random.randint(2500, 5000)

    else:
        return 0


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("OID manquant", file=sys.stderr)
        sys.exit(1)

    oid = sys.argv[1]

    value = generate_metric(oid)

    print(value)
