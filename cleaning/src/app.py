from flask import Flask, request, jsonify
from flask_cors import CORS
from repository import Repository
from validator import validate_metrics
from cleaner import clean_metrics
from normalizer import normalize_metrics
from enricher import enrich_metrics
from anomaly_detector import detect_anomalies
from review_manager import review_metrics
from logger import log_processing
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import csv
import tempfile
from server_repository import ServerRepository
from ups_repository import UPSRepository
from cooling_repository import CoolingRepository
app = Flask(__name__)
CORS(app)
repository = Repository()
server_repository = ServerRepository()
ups_repository = UPSRepository()
cooling_repository = CoolingRepository()

server_repository = ServerRepository()
ups_repository = UPSRepository()
cooling_repository = CoolingRepository()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "Cleaning Service is running"
    })


@app.route("/metrics", methods=["GET"])
def get_metrics():

    metrics = repository.get_all()

    return jsonify(metrics), 200

@app.route("/metrics/critical", methods=["GET"])
def get_critical_metrics():

    metrics = repository.get_critical_metrics()

    return jsonify(metrics), 200

@app.route("/metrics/warning", methods=["GET"])
def get_warning_metrics():

    metrics = repository.get_warning_metrics()

    return jsonify(metrics), 200

@app.route("/metrics/ok", methods=["GET"])
def get_ok_metrics():

    metrics = repository.get_ok_metrics()

    return jsonify(metrics), 200


@app.route("/metrics/switches", methods=["GET"])
def get_switchs():
    return jsonify(repository.get_switchs()), 200
@app.route("/metrics/routeur", methods=["GET"])
def get_routeur():
    return jsonify(repository.get_routeur()), 200

@app.route("/metrics/all", methods=["GET"])
def get_all():
    return jsonify(repository.get_all()), 200

@app.route("/metrics/firewall", methods=["GET"])
def get_firewall():
    return jsonify(repository.get_firewall()), 200

@app.route("/dashboard/statistics", methods=["GET"])
def get_dashboard_statistics():

    statistics = repository.get_dashboard_statistics()

    return jsonify(statistics), 200

@app.route("/metrics/<hostname>", methods=["GET"])
def get_metrics_by_equipment(hostname):

    metrics = repository.get_metrics_by_equipment(hostname)

    return jsonify(metrics), 200

@app.route("/metrics/last50", methods=["GET"])
def get_last_50_metrics():

    metrics = repository.get_last_50_metrics()

    return jsonify(metrics), 200

@app.route("/statistics/cpu-history", methods=["GET"])
def cpu_history():

    return jsonify(repository.get_cpu_history()), 200

@app.route("/statistics/temperature-history", methods=["GET"])
def temperature_history():

    return jsonify(repository.get_temperature_history()), 200

@app.route("/statistics/power-history", methods=["GET"])
def power_history():

    return jsonify(repository.get_power_history()), 200

@app.route("/export/csv", methods=["GET"])
def export_csv():

    metrics = repository.get_all()

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")

    writer = csv.writer(temp)

    writer.writerow([
        "Hostname",
        "Type",
        "CPU",
        "RAM",
        "Disk",
        "Temperature",
        "Power",
        "Status"
    ])

    for metric in metrics:

        writer.writerow([
            metric["hostname"],
            metric["type"],
            metric["cpu"],
            metric["ram"],
            metric["disk"],
            metric["temperature"],
            metric["power"],
            metric["status"]
        ])

    temp.close()

    return send_file(
        temp.name,
        as_attachment=True,
        download_name="metrics.csv",
        mimetype="text/csv"
    )

@app.route("/statistics", methods=["GET"])
def get_statistics():

    return jsonify(repository.get_dashboard_statistics()), 200

@app.route("/export/pdf", methods=["GET"])
def export_pdf():

    statistics = repository.get_dashboard_statistics()

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp.name)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>DATA CENTER MONITORING REPORT</b>", styles["Title"]))

    story.append(Paragraph(f"Total équipements : {statistics['total_equipments']}", styles["BodyText"]))
    story.append(Paragraph(f"CPU moyen : {statistics['averages']['cpu']} %", styles["BodyText"]))
    story.append(Paragraph(f"RAM moyenne : {statistics['averages']['ram']} %", styles["BodyText"]))
    story.append(Paragraph(f"Température moyenne : {statistics['averages']['temperature']} °C", styles["BodyText"]))
    story.append(Paragraph(f"Puissance moyenne : {statistics['averages']['power']} W", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Répartition des statuts</b>", styles["Heading2"]))

    for status, count in statistics["by_status"].items():

        story.append(
            Paragraph(f"{status} : {count}", styles["BodyText"])
        )

    doc.build(story)

    temp.close()

    return send_file(
        temp.name,
        as_attachment=True,
        download_name="monitoring_report.pdf",
        mimetype="application/pdf"
    )
@app.route("/metrics", methods=["POST"])
def receive_metrics():

    # ==========================
    # Réception
    # ==========================

    data = request.get_json()

    if data is None:
        return jsonify({
            "error": "Aucune donnée reçue."
        }), 400

    # ==========================
    # Validation
    # ==========================

    valid, message = validate_metrics(data)

    if not valid:
        
        print("ERREUR VALIDATION :", message)
        print(data)
        
        return jsonify({
            "status": "error",
            "message": message
        }), 400

    # ==========================
    # Cleaning
    # ==========================

    cleaned = clean_metrics(data)

    # ==========================
    # Normalization
    # ==========================

    normalized = normalize_metrics(cleaned)

    # ==========================
    # Enrichment
    # ==========================

    enriched = enrich_metrics(normalized)

    # ==========================
    # Détection d'anomalies
    # ==========================

    anomalies = detect_anomalies(enriched)

    # ==========================
    # Review Manager
    # ==========================

    reviewed = review_metrics(enriched, anomalies)

    # ==========================
    # Logger
    # ==========================

    log_processing(reviewed, anomalies)
    
    print("Avant save_metrics")

    if reviewed["type"] == "SERVER":
       server_repository.save(reviewed)

    elif reviewed["type"] == "UPS":
       ups_repository.save(reviewed)

    elif reviewed["type"] == "COOLING":
        cooling_repository.save(reviewed)
    print("Après save_metrics")
    # ==========================
    # Réponse
    # ==========================

    return jsonify({
        "status": "success",
        "review_status": reviewed["review_status"],
        "anomalies": anomalies,
        "data": reviewed
    }), 200

# ==========================================
# SERVER METRICS
# ==========================================

@app.route("/servers", methods=["GET"])
def get_servers():

    data = repository.get_server_metrics()

    return jsonify(data)


# ==========================================
# UPS METRICS
# ==========================================

@app.route("/ups", methods=["GET"])
def get_ups():

    data = repository.get_ups_metrics()

    return jsonify(data)


# ==========================================
# COOLING METRICS
# ==========================================

@app.route("/cooling", methods=["GET"])
def get_cooling():

    data = repository.get_cooling_metrics()

    return jsonify(data)

@app.route("/statistics/servers", methods=["GET"])
def server_statistics():

    return jsonify(repository.get_server_statistics())


@app.route("/statistics/ups", methods=["GET"])
def ups_statistics():

    return jsonify(repository.get_ups_statistics())


@app.route("/statistics/cooling", methods=["GET"])
def cooling_statistics():

    return jsonify(repository.get_cooling_statistics())
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
