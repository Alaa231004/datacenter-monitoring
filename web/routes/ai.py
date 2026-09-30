import re

from flask import Blueprint, request, jsonify
from services.database import fetch_all


ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


# ================================================================
# ACCÈS DONNÉES
# ================================================================
# On récupère toujours l'état ACTUEL (1 ligne par hostname), et non
# les 20 dernières lignes brutes qui peuvent contenir plusieurs
# mesures successives du même équipement et fausser les comptages.

def latest_metrics(table):
    allowed_tables = {
        "server_metrics",
        "ups_metrics",
        "cooling_metrics",
    }

    if table not in allowed_tables:
        raise ValueError("Table non autorisée")

    return fetch_all(f"""
        SELECT DISTINCT ON (hostname) *
        FROM {table}
        ORDER BY hostname, timestamp DESC
    """)


def load_all_equipment():
    return {
        "servers": latest_metrics("server_metrics"),
        "ups": latest_metrics("ups_metrics"),
        "cooling": latest_metrics("cooling_metrics"),
    }


EQUIPMENT_LABELS = {
    "servers": "serveur(s)",
    "ups": "UPS",
    "cooling": "équipement(s) de refroidissement",
}


# ================================================================
# DÉTECTION DU TYPE D'ÉQUIPEMENT CIBLÉ PAR LA QUESTION
# ================================================================

EQUIPMENT_KEYWORDS = {
    "servers": ["serveur", "server", "srv", "cpu", "ram", "mémoire", "memoire"],
    "ups": ["ups", "onduleur", "batterie", "battery"],
    "cooling": [
        "cooling", "climatisation", "clim", "refroidissement",
        "ventilateur", "humidité", "humidite", "pression",
    ],
}


def detect_scope(question, equipment):
    """
    Retourne la liste des clés ('servers', 'ups', 'cooling') visées
    par la question. Si aucun mot-clé spécifique n'est trouvé,
    retourne les trois (portée globale).
    """

    matched = []

    for key, keywords in EQUIPMENT_KEYWORDS.items():
        if any(word in question for word in keywords):
            matched.append(key)

    if not matched:
        matched = list(equipment.keys())

    return matched


# ================================================================
# UTILITAIRES
# ================================================================

def is_status(row, value):
    return str(row.get("status", "")).upper() == value


def is_risk(row, value):
    return str(row.get("risk_level", "")).upper() == value


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def format_value(value, unit=""):
    if value is None:
        return "--"
    return f"{value:.1f}{unit}"


def list_hostnames(rows, limit=5):
    names = [str(row.get("hostname", "?")) for row in rows[:limit]]
    remainder = len(rows) - len(names)

    text = ", ".join(names)

    if remainder > 0:
        text += f" (+{remainder} autre(s))"

    return text


# Métriques disponibles par type d'équipement, avec leurs synonymes
# en français et l'unité à afficher.
METRICS = {
    "servers": {
        "cpu": (["cpu", "processeur"], "%"),
        "ram": (["ram", "mémoire", "memoire"], "%"),
        "temperature": (["température", "temperature", "temp", "chaud", "chaleur"], "°C"),
        "power": (["puissance", "power", "consommation", "consomme"], "W"),
    },
    "ups": {
        "battery_level": (["batterie", "battery", "charge"], "%"),
        "runtime": (["runtime", "autonomie"], "min"),
        "load": (["charge", "load"], "%"),
        "temperature": (["température", "temperature", "temp"], "°C"),
        "power": (["puissance", "power", "consommation", "consomme"], "W"),
    },
    "cooling": {
        "supply_temperature": (["soufflage", "supply"], "°C"),
        "return_temperature": (["retour", "return"], "°C"),
        "humidity": (["humidité", "humidite"], "%"),
        "fan_speed": (["ventilateur", "fan"], "RPM"),
        "power": (["puissance", "power", "consommation", "consomme"], "W"),
        "pressure": (["pression", "pressure"], ""),
    },
}


def detect_metric(question, scope):
    """
    Cherche dans la question un mot-clé correspondant à une métrique
    connue pour au moins un des types d'équipement de la portée.
    Retourne (metric_key, unit) ou (None, None).
    """

    for key in scope:
        for metric_key, (keywords, unit) in METRICS.get(key, {}).items():
            if any(word in question for word in keywords):
                return metric_key, unit

    return None, None


# ================================================================
# RECHERCHE D'UN ÉQUIPEMENT PAR HOSTNAME
# ================================================================

def find_hostname_match(question, equipment):
    tokens = re.findall(r"[a-zA-Z0-9\-_]+", question)

    for key, rows in equipment.items():
        for row in rows:
            hostname = str(row.get("hostname", ""))

            if not hostname:
                continue

            if hostname.lower() in [token.lower() for token in tokens]:
                return key, row

    return None, None


def describe_row(key, row):
    hostname = row.get("hostname", "?")
    status = str(row.get("status", "--")).upper()

    if key == "servers":
        return (
            f"<strong>{hostname}</strong> (serveur) — statut {status}, "
            f"risque {str(row.get('risk_level', '--')).upper()}<br>"
            f"CPU {format_value(safe_float(row.get('cpu')), '%')} · "
            f"RAM {format_value(safe_float(row.get('ram')), '%')} · "
            f"Température {format_value(safe_float(row.get('temperature')), '°C')} · "
            f"Puissance {format_value(safe_float(row.get('power')), 'W')} · "
            f"Anomalies : {row.get('anomaly_count', 0)}"
        )

    if key == "ups":
        return (
            f"<strong>{hostname}</strong> (UPS) — statut {status}, "
            f"risque {str(row.get('risk_level', '--')).upper()}<br>"
            f"Batterie {format_value(safe_float(row.get('battery_level')), '%')} · "
            f"Autonomie {format_value(safe_float(row.get('runtime')), ' min')} · "
            f"Charge {format_value(safe_float(row.get('load')), '%')} · "
            f"Anomalies : {row.get('anomaly_count', 0)}"
        )

    return (
        f"<strong>{hostname}</strong> (cooling) — statut {status}<br>"
        f"Soufflage {format_value(safe_float(row.get('supply_temperature')), '°C')} · "
        f"Retour {format_value(safe_float(row.get('return_temperature')), '°C')} · "
        f"Humidité {format_value(safe_float(row.get('humidity')), '%')} · "
        f"Anomalies : {row.get('anomaly_count', 0)}"
    )


# ================================================================
# GESTIONNAIRES D'INTENTIONS
# ================================================================

def handle_greeting():
    return (
        "Bonjour 👋 Je suis l'assistant du Data Center. "
        "Je peux vous renseigner sur les serveurs, les UPS et le "
        "refroidissement : effectifs, équipements en alerte, "
        "anomalies, moyennes, valeurs extrêmes, ou l'état d'un "
        "hostname précis. Que voulez-vous savoir ?"
    )


def handle_help():
    return (
        "Voici ce que je peux faire :<br>"
        "• <em>Effectifs</em> — « Combien de serveurs / UPS avons-nous ? »<br>"
        "• <em>Alertes</em> — « Y a-t-il des équipements critiques ? », "
        "« Combien d'avertissements côté cooling ? »<br>"
        "• <em>Anomalies</em> — « Y a-t-il des anomalies sur les UPS ? »<br>"
        "• <em>Statistiques</em> — « Quelle est la température moyenne des "
        "serveurs ? », « Quel serveur consomme le plus de puissance ? »<br>"
        "• <em>Risque</em> — « Combien d'équipements à risque élevé ? »<br>"
        "• <em>Un équipement précis</em> — donnez son hostname, ex. « État de SRV-004 »<br>"
        "• <em>Résumé</em> — « Fais-moi un résumé de l'état du data center »"
    )


def handle_count(scope, equipment):
    parts = []

    for key in scope:
        rows = equipment[key]
        parts.append(f"{len(rows)} {EQUIPMENT_LABELS[key]}")

    return "Le système contient actuellement " + ", ".join(parts) + " (dernières mesures)."


def handle_status_filter(scope, equipment, status_value, label):
    total = 0
    details = []

    for key in scope:
        matches = [row for row in equipment[key] if is_status(row, status_value)]
        total += len(matches)

        if matches:
            details.append(
                f"{EQUIPMENT_LABELS[key]} : {len(matches)} "
                f"({list_hostnames(matches)})"
            )

    if total == 0:
        return f"Aucun équipement en état {label} actuellement. Tout va bien de ce côté-là. ✅"

    answer = f"J'ai détecté {total} équipement(s) en état {label} :<br>"
    answer += "<br>".join(details)
    return answer


def handle_risk(scope, equipment, risk_value):
    total = 0
    details = []

    for key in scope:
        if key == "cooling":
            continue  # pas de risk_level sur le cooling

        matches = [row for row in equipment[key] if is_risk(row, risk_value)]
        total += len(matches)

        if matches:
            details.append(
                f"{EQUIPMENT_LABELS[key]} : {len(matches)} "
                f"({list_hostnames(matches)})"
            )

    if total == 0:
        return f"Aucun équipement à risque {risk_value} actuellement."

    answer = f"{total} équipement(s) à risque {risk_value} :<br>"
    answer += "<br>".join(details)
    return answer


def handle_anomalies(scope, equipment):
    total = 0
    worst = []

    for key in scope:
        for row in equipment[key]:
            count = int(row.get("anomaly_count") or 0)
            total += count

            if count > 0:
                worst.append((count, key, row))

    if total == 0:
        return "Aucune anomalie détectée dans les dernières mesures. 👍"

    worst.sort(key=lambda item: item[0], reverse=True)
    top = worst[:5]

    lines = [
        f"{row.get('hostname', '?')} ({EQUIPMENT_LABELS[key]}) — {count} anomalie(s)"
        for count, key, row in top
    ]

    answer = f"Le nombre total d'anomalies est de {total}.<br>Top équipements concernés :<br>"
    answer += "<br>".join(lines)
    return answer


def handle_average(scope, equipment, metric, unit):
    lines = []

    for key in scope:
        if metric not in METRICS.get(key, {}):
            continue

        values = [
            safe_float(row.get(metric))
            for row in equipment[key]
            if safe_float(row.get(metric)) is not None
        ]

        if not values:
            continue

        average = sum(values) / len(values)
        lines.append(f"{EQUIPMENT_LABELS[key]} : {format_value(average, unit)}")

    if not lines:
        return "Je n'ai pas trouvé de données pour calculer cette moyenne."

    return "Moyenne actuelle —<br>" + "<br>".join(lines)


def handle_extreme(scope, equipment, metric, unit, want_max):
    best_row = None
    best_key = None
    best_value = None

    for key in scope:
        if metric not in METRICS.get(key, {}):
            continue

        for row in equipment[key]:
            value = safe_float(row.get(metric))

            if value is None:
                continue

            if best_value is None or (value > best_value if want_max else value < best_value):
                best_value = value
                best_row = row
                best_key = key

    if best_row is None:
        return "Je n'ai pas trouvé de données pour répondre à cette question."

    superlative = "le plus élevé" if want_max else "le plus bas"

    return (
        f"C'est <strong>{best_row.get('hostname', '?')}</strong> "
        f"({EQUIPMENT_LABELS[best_key]}) qui a la valeur {superlative} : "
        f"{format_value(best_value, unit)}."
    )


def handle_summary(equipment):
    total = sum(len(rows) for rows in equipment.values())

    critical = sum(
        1 for rows in equipment.values() for row in rows if is_status(row, "CRITICAL")
    )

    warning = sum(
        1 for rows in equipment.values() for row in rows if is_status(row, "WARNING")
    )

    anomalies = sum(
        int(row.get("anomaly_count") or 0)
        for rows in equipment.values()
        for row in rows
    )

    health = "🟢 Tout va bien"

    if critical > 0:
        health = "🔴 Attention requise"
    elif warning > 0:
        health = "🟠 Surveillance recommandée"

    return (
        f"Résumé du Data Center — {health}<br>"
        f"• {total} équipement(s) au total "
        f"({len(equipment['servers'])} serveurs, {len(equipment['ups'])} UPS, "
        f"{len(equipment['cooling'])} cooling)<br>"
        f"• {critical} en état CRITICAL, {warning} en état WARNING<br>"
        f"• {anomalies} anomalie(s) détectée(s) au total"
    )


# ================================================================
# ROUTE PRINCIPALE
# ================================================================

@ai_bp.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json()
        question = (data.get("question") or "").strip()

        if not question:
            return jsonify({"error": "Question vide"}), 400

        q = question.lower()

        equipment = load_all_equipment()
        scope = detect_scope(q, equipment)

        # ------------------------------------------------------
        # SALUTATIONS / AIDE
        # ------------------------------------------------------

        if any(word in q for word in ["bonjour", "salut", "hello", "coucou", "hey"]):
            answer = handle_greeting()

        elif any(word in q for word in ["aide", "help", "capable", "peux-tu", "peux tu"]):
            answer = handle_help()

        # ------------------------------------------------------
        # RÉSUMÉ GLOBAL
        # ------------------------------------------------------

        elif any(word in q for word in ["résumé", "resume", "summary", "vue d'ensemble", "état général", "etat general"]):
            answer = handle_summary(equipment)

        # ------------------------------------------------------
        # ÉQUIPEMENT PRÉCIS (par hostname)
        # ------------------------------------------------------

        elif find_hostname_match(q, equipment)[1] is not None:
            key, row = find_hostname_match(q, equipment)
            answer = describe_row(key, row)

        # ------------------------------------------------------
        # ANOMALIES
        # ------------------------------------------------------

        elif "anomal" in q:
            answer = handle_anomalies(scope, equipment)

        # ------------------------------------------------------
        # STATUTS (critique / warning / ok)
        # ------------------------------------------------------

        elif any(word in q for word in ["critique", "critical", "en panne", "panne"]):
            answer = handle_status_filter(scope, equipment, "CRITICAL", "CRITICAL")

        elif any(word in q for word in ["avertissement", "warning", "alerte"]):
            answer = handle_status_filter(scope, equipment, "WARNING", "WARNING")

        elif any(word in q for word in ["opérationnel", "operationnel", " ok ", "sain", "normal"]):
            answer = handle_status_filter(scope, equipment, "OK", "OK")

        # ------------------------------------------------------
        # NIVEAU DE RISQUE
        # ------------------------------------------------------

        elif "risque" in q or "risk" in q:
            if any(word in q for word in ["élevé", "eleve", "high", "fort"]):
                answer = handle_risk(scope, equipment, "HIGH")
            elif any(word in q for word in ["faible", "low", "bas"]):
                answer = handle_risk(scope, equipment, "LOW")
            else:
                answer = handle_risk(scope, equipment, "MEDIUM")

        # ------------------------------------------------------
        # VALEURS EXTRÊMES (max / min)
        # ------------------------------------------------------

        elif any(word in q for word in ["plus élevé", "plus eleve", "maximum", "max", "le plus chaud", "pire", "plus grande", "plus consomme", "plus haute"]):
            metric, unit = detect_metric(q, scope)

            if metric:
                answer = handle_extreme(scope, equipment, metric, unit, want_max=True)
            else:
                answer = (
                    "Je n'ai pas identifié la métrique visée. Essayez par exemple : "
                    "« Quel serveur a la température la plus élevée ? »"
                )

        elif any(word in q for word in ["plus bas", "plus basse", "minimum", "min", "le plus froid"]):
            metric, unit = detect_metric(q, scope)

            if metric:
                answer = handle_extreme(scope, equipment, metric, unit, want_max=False)
            else:
                answer = (
                    "Je n'ai pas identifié la métrique visée. Essayez par exemple : "
                    "« Quel serveur a la température la plus basse ? »"
                )

        # ------------------------------------------------------
        # MOYENNES
        # ------------------------------------------------------

        elif any(word in q for word in ["moyenne", "average", "en moyenne"]):
            metric, unit = detect_metric(q, scope)

            if metric:
                answer = handle_average(scope, equipment, metric, unit)
            else:
                answer = (
                    "Je n'ai pas identifié la métrique visée. Essayez par exemple : "
                    "« Quelle est la température moyenne des serveurs ? »"
                )

        # ------------------------------------------------------
        # EFFECTIFS (combien de ...)
        # ------------------------------------------------------

        elif "combien" in q or "nombre" in q:
            answer = handle_count(scope, equipment)

        # ------------------------------------------------------
        # PAR DÉFAUT
        # ------------------------------------------------------

        else:
            answer = (
                "Je n'ai pas bien compris la question. Vous pouvez par exemple demander :<br>"
                "« Combien de serveurs sont critiques ? »<br>"
                "« Quelle est la température moyenne des serveurs ? »<br>"
                "« Y a-t-il des anomalies sur les UPS ? »<br>"
                "« Fais-moi un résumé de l'état du data center »"
            )

        return jsonify({"answer": answer})

    except Exception as error:
        print("Erreur AI:", error)
        return jsonify({"error": str(error)}), 500
