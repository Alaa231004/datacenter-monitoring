from flask import Blueprint, jsonify, request

from services.metrics_service import (
    get_servers,
    get_ups,
    get_cooling
)

equipment_bp = Blueprint(
    "equipment",
    __name__,
    url_prefix="/api/equipment"
)


def get_filters():

    return {
        "hostname": request.args.get("hostname"),
        "status": request.args.get("status"),
        "risk_level": request.args.get("risk_level"),
        "equipment_type": request.args.get("equipment_type")
    }


@equipment_bp.route("/servers", methods=["GET"])
def servers():

    data = get_servers(get_filters())

    return jsonify(data)


@equipment_bp.route("/ups", methods=["GET"])
def ups():

    data = get_ups(get_filters())

    return jsonify(data)


@equipment_bp.route("/cooling", methods=["GET"])
def cooling():

    data = get_cooling(get_filters())

    return jsonify(data)
