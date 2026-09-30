import json
from pathlib import Path


DATA_FILE = Path("../simulator/data/device_state.json")


def load_data():

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def get_metric(hostname, metric):

    data = load_data()

    if hostname not in data:
        return None

    if metric not in data[hostname]:
        return None

    return data[hostname][metric]
