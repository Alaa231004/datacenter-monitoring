import os

from flask import (
    Flask,
    jsonify,
    render_template,
    session,
    redirect,
    url_for
)

from routes.equipment import equipment_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)


# ============================================================
# SECRET KEY
# ============================================================

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret-key-change-me"
)


# ============================================================
# CONFIGURATION
# ============================================================

app.config["JSON_SORT_KEYS"] = False


# ============================================================
# BLUEPRINTS
# ============================================================

app.register_blueprint(equipment_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "service": "datacenter-web"
    })


# ============================================================
# HOME / PROTECTED DASHBOARD
# ============================================================

@app.route("/")
def home():

    # Si l'utilisateur n'est pas connecté
    if "user_id" not in session:

        return redirect(
            url_for("auth.login_page")
        )

    # Utilisateur connecté
    return render_template("index.html")


# ============================================================
# APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
