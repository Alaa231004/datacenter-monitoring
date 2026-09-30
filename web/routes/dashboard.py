from flask import Blueprint, jsonify

from services.metrics_service import get_dashboard_statistics


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.route("/statistics", methods=["GET"])
def statistics():

    data = get_dashboard_statistics()

    return jsonify(data)
