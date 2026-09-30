import random
from datetime import datetime, timedelta
import string
import random
import secrets
from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    redirect,
    url_for
)
from services.email_service import send_verification_email, send_new_account_email
from werkzeug.security import generate_password_hash, check_password_hash
from services.database import get_connection, fetch_all
from services.email_service import send_verification_email
from functools import wraps

def generate_temp_password(length=12):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        if session.get("role") != "ADMIN":
            return jsonify({
                "success": False,
                "message": "Accès réservé aux administrateurs."
            }), 403
        return f(*args, **kwargs)
    return decorated

auth_bp = Blueprint("auth", __name__)


# ============================================================
# REGISTER PAGE
# ============================================================

# ============================================================
# REGISTER (DÉSACTIVÉ - création par admin uniquement)
# ============================================================
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    return jsonify({
        "success": False,
        "message": "L'inscription publique est désactivée. Contactez un administrateur."
    }), 403

# ============================================================
# VERIFY EMAIL PAGE
# ============================================================

@auth_bp.route("/verify-email", methods=["GET"])
def verify_email_page():

    if "verification_user_id" not in session:

        return redirect(
            url_for("auth.register_page")
        )

    return render_template("verify_email.html")


# ============================================================
# VERIFY EMAIL
# ============================================================

@auth_bp.route("/api/auth/verify", methods=["POST"])
def verify_email():

    data = request.get_json()

    code = data.get("code", "").strip()

    user_id = session.get(
        "verification_user_id"
    )

    if not user_id:

        return jsonify({
            "success": False,
            "message": "Session de vérification expirée."
        }), 401


    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    verification_code,
                    verification_expires
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:

                return jsonify({
                    "success": False,
                    "message": "Utilisateur introuvable."
                }), 404


            verification_code = user[0]
            verification_expires = user[1]


            if datetime.now() > verification_expires:

                return jsonify({
                    "success": False,
                    "message": "Le code a expiré."
                }), 400


            if code != verification_code:

                return jsonify({
                    "success": False,
                    "message": "Code incorrect."
                }), 400


            cursor.execute(
                """
                UPDATE users
                SET
                    email_verified = TRUE,
                    verification_code = NULL,
                    verification_expires = NULL
                WHERE id = %s
                """,
                (user_id,)
            )

            connection.commit()


        session.pop(
            "verification_user_id",
            None
        )


        return jsonify({
            "success": True,
            "message": "Email vérifié.",
            "redirect": "/login"
        })


    except Exception as error:

        connection.rollback()

        print("VERIFY ERROR:", error)

        return jsonify({
            "success": False,
            "message": "Erreur de vérification."
        }), 500


    finally:

        connection.close()


# ============================================================
# LOGIN PAGE
# ============================================================

@auth_bp.route("/login", methods=["GET"])
def login_page():

    return render_template("login.html")


# ============================================================
# LOGIN
# ============================================================

# ============================================================
# LOGIN
# ============================================================
@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    identifier = data.get(
        "identifier",
        ""
    ).strip().lower()
    password = data.get(
        "password",
        ""
    )
    if not identifier or not password:
        return jsonify({
            "success": False,
            "message": "Veuillez remplir tous les champs."
        }), 400
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    email,
                    password_hash,
                    email_verified,
                    role,
                    must_change_password
                FROM users
                WHERE LOWER(username) = %s
                   OR LOWER(email) = %s
                """,
                (
                    identifier,
                    identifier
                )
            )
            user = cursor.fetchone()
        if not user:
            return jsonify({
                "success": False,
                "message": "Identifiants incorrects."
            }), 401
        user_id = user[0]
        username = user[1]
        password_hash = user[3]
        email_verified = user[4]
        role = user[5]
        must_change_password = user[6]
        if not check_password_hash(
            password_hash,
            password
        ):
            return jsonify({
                "success": False,
                "message": "Identifiants incorrects."
            }), 401
        if not email_verified:
            session[
                "verification_user_id"
            ] = user_id
            return jsonify({
                "success": False,
                "message": "Veuillez vérifier votre email.",
                "redirect": "/verify-email"
            }), 403
        session.clear()
        session["user_id"] = user_id
        session["username"] = username
        session["role"] = role
        if must_change_password:
            session["must_change_password"] = True
            return jsonify({
                "success": True,
                "message": "Connexion réussie.",
                "redirect": "/change-password"
            })
        return jsonify({
            "success": True,
            "message": "Connexion réussie.",
            "redirect": "/"
        })
    except Exception as error:
        print("LOGIN ERROR:", error)
        return jsonify({
            "success": False,
            "message": "Erreur de connexion."
        }), 500
    finally:
        connection.close()

# ============================================================
# LOGOUT
# ============================================================

@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "redirect": "/login"
    })


# ============================================================
# ADMIN - PAGE GESTION UTILISATEURS
# ============================================================
@auth_bp.route("/admin/users", methods=["GET"])
@admin_required
def admin_users_page():
    users = fetch_all(
        """
        SELECT id, username, email, role, is_active, created_at
        FROM users
        ORDER BY created_at DESC
        """
    )
    return render_template("admin_users.html", users=users)

# ============================================================
# ADMIN - CRÉER UN EMPLOYÉ
# ============================================================
@auth_bp.route("/api/admin/users", methods=["POST"])
@admin_required
def admin_create_user():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()

    if not username or not email:
        return jsonify({
            "success": False,
            "message": "Nom d'utilisateur et email obligatoires."
        }), 400

    temp_password = generate_temp_password()
    password_hash = generate_password_hash(temp_password)

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id FROM users WHERE username = %s OR email = %s
                """,
                (username, email)
            )
            if cursor.fetchone():
                return jsonify({
                    "success": False,
                    "message": "Username ou email déjà utilisé."
                }), 409

            cursor.execute(
                """
                INSERT INTO users (
                    username, email, password_hash,
                    role, is_active, must_change_password,
                    email_verified
                )
                VALUES (%s, %s, %s, 'EMPLOYEE', TRUE, TRUE, TRUE)
                RETURNING id
                """,
                (username, email, password_hash)
            )
            new_user_id = cursor.fetchone()[0]
            connection.commit()

        try:
            send_new_account_email(
                recipient_email=email,
                username=username,
                temp_password=temp_password
            )
        except Exception as email_error:
            print("EMAIL ERROR:", email_error)
            return jsonify({
                "success": True,
                "message": (
                    "Compte créé mais l'email n'a pas pu être envoyé. "
                    f"Mot de passe temporaire : {temp_password}"
                )
            })

        return jsonify({
            "success": True,
            "message": f"Compte créé pour {username}. Email envoyé."
        })
    except Exception as error:
        connection.rollback()
        print("ADMIN CREATE USER ERROR:", error)
        return jsonify({
            "success": False,
            "message": "Erreur lors de la création du compte."
        }), 500
    finally:
        connection.close()

# ============================================================
# CHANGE PASSWORD (première connexion obligatoire)
# ============================================================
@auth_bp.route("/change-password", methods=["GET"])
def change_password_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("change_password.html")


@auth_bp.route("/api/auth/change-password", methods=["POST"])
def change_password():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Session expirée."
        }), 401

    data = request.get_json() or {}
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "Le mot de passe doit contenir au moins 8 caractères."
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Les mots de passe ne correspondent pas."
        }), 400

    password_hash = generate_password_hash(new_password)
    user_id = session["user_id"]

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE users
                SET password_hash = %s, must_change_password = FALSE
                WHERE id = %s
                """,
                (password_hash, user_id)
            )
            connection.commit()
        session.pop("must_change_password", None)
        return jsonify({
            "success": True,
            "message": "Mot de passe modifié avec succès.",
            "redirect": "/"
        })
    except Exception as error:
        connection.rollback()
        print("CHANGE PASSWORD ERROR:", error)
        return jsonify({
            "success": False,
            "message": "Erreur lors de la modification."
        }), 500
    finally:
        connection.close()
