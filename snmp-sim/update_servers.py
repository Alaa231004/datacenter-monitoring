from pathlib import Path
import os

DATA_DIR = Path(os.getenv("SNMP_DATA_DIR", "/app/data"))

OIDS = {
    "1.3.6.1.4.1.2021.11.9.0",       # CPU
    "1.3.6.1.4.1.2021.4.6.0",        # RAM
    "1.3.6.1.4.1.2021.13.16.2.1.3.1",# Temperature
    "1.3.6.1.4.1.2021.9.1.0",        # Disk
    "1.3.6.1.4.1.2021.10.1.0",       # Power
    "1.3.6.1.4.1.2021.11.1.0",       # Network IN
    "1.3.6.1.4.1.2021.11.2.0",       # Network OUT
    "1.3.6.1.4.1.2021.12.1.0",       # Fan Speed
}


for server in ["srv002.snmprec", "srv003.snmprec"]:

    file_path = DATA_DIR / server

    lines = file_path.read_text().splitlines()
    new_lines = []

    for line in lines:

        parts = line.split("|")

        if len(parts) >= 3 and parts[0] in OIDS:

            oid = parts[0]

            new_lines.append(
                f"{oid}|2:subprocess|python3 "
                f"{DATA_DIR.parent}/dynamic_metrics.py @OID@"
            )

        else:
            new_lines.append(line)

    file_path.write_text("\n".join(new_lines) + "\n")

    print(f"✅ {server} rendu dynamique")
