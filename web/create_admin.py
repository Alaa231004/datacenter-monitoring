# create_admin.py
"""
Script à exécuter UNE SEULE FOIS pour créer le premier compte administrateur.
Usage: python3 create_admin.py
"""
import getpass
from werkzeug.security import generate_password_hash
from services.database import get_connection

def create_admin():
    username = input("Username admin : ").strip()
    email = input("Email admin : ").strip().lower()
    password = getpass.getpass("Mot de passe admin (min 8 caractères) : ")

    if len(password) < 8:
        print("Erreur : le mot de passe doit faire au moins 8 caractères.")
        return

    password_hash = generate_password_hash(password)

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
                print("Erreur : ce username ou cet email existe déjà.")
                return

            cursor.execute(
                """
                INSERT INTO users (
                    username, email, password_hash,
                    role, is_active, must_change_password,
                    email_verified
                )
                VALUES (%s, %s, %s, 'ADMIN', TRUE, FALSE, TRUE)
                RETURNING id
                """,
                (username, email, password_hash)
            )
            admin_id = cursor.fetchone()[0]
            connection.commit()
            print(f"✅ Compte admin créé avec succès (id={admin_id}).")
    except Exception as e:
        connection.rollback()
        print("Erreur :", e)
    finally:
        connection.close()

if __name__ == "__main__":
    create_admin()
