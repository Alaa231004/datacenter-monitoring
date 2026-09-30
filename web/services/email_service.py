import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


load_dotenv()


def send_verification_email(
    recipient_email,
    username,
    verification_code
):

    smtp_server = os.getenv(
        "SMTP_SERVER"
    )

    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )

    smtp_username = os.getenv(
        "SMTP_USERNAME"
    )

    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )

    smtp_from = os.getenv(
        "SMTP_FROM",
        smtp_username
    )


    if not smtp_server:
        raise Exception(
            "SMTP_SERVER n'est pas configuré."
        )

    if not smtp_username:
        raise Exception(
            "SMTP_USERNAME n'est pas configuré."
        )

    if not smtp_password:
        raise Exception(
            "SMTP_PASSWORD n'est pas configuré."
        )


    subject = "Vérification de votre compte - Data Center Monitoring"


    html = f"""
    <!DOCTYPE html>

    <html>

    <body style="
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        padding: 40px;
    ">

        <div style="
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        ">

            <h2>
                Data Center Monitoring
            </h2>

            <p>
                Bonjour <strong>{username}</strong>,
            </p>

            <p>
                Merci d'avoir créé votre compte.
            </p>

            <p>
                Votre code de vérification est :
            </p>

            <div style="
                font-size: 32px;
                font-weight: bold;
                letter-spacing: 8px;
                text-align: center;
                padding: 20px;
                background: #f1f5ff;
                border-radius: 8px;
            ">

                {verification_code}

            </div>

            <p>
                Ce code est valable pendant
                <strong>10 minutes</strong>.
            </p>

            <p>
                Si vous n'êtes pas à l'origine de cette
                inscription, vous pouvez ignorer cet email.
            </p>

            <hr>

            <p style="
                color: #777;
                font-size: 12px;
            ">

                Data Center Monitoring Platform

            </p>

        </div>

    </body>

    </html>
    """


    message = MIMEMultipart("alternative")

    message["Subject"] = subject
    message["From"] = smtp_from
    message["To"] = recipient_email

    message.attach(
        MIMEText(
            html,
            "html"
        )
    )


    with smtplib.SMTP(
        smtp_server,
        smtp_port
    ) as server:

        server.starttls()

        server.login(
            smtp_username,
            smtp_password
        )

        server.sendmail(
            smtp_from,
            recipient_email,
            message.as_string()
        )


    return True

def send_new_account_email(
    recipient_email,
    username,
    temp_password
):
    smtp_server = os.getenv(
        "SMTP_SERVER"
    )
    smtp_port = int(
        os.getenv(
            "SMTP_PORT",
            "587"
        )
    )
    smtp_username = os.getenv(
        "SMTP_USERNAME"
    )
    smtp_password = os.getenv(
        "SMTP_PASSWORD"
    )
    smtp_from = os.getenv(
        "SMTP_FROM",
        smtp_username
    )
    if not smtp_server:
        raise Exception(
            "SMTP_SERVER n'est pas configuré."
        )
    if not smtp_username:
        raise Exception(
            "SMTP_USERNAME n'est pas configuré."
        )
    if not smtp_password:
        raise Exception(
            "SMTP_PASSWORD n'est pas configuré."
        )
    subject = "Votre compte a été créé - Data Center Monitoring"
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="
        font-family: Arial, sans-serif;
        background: #f4f7fb;
        padding: 40px;
    ">
        <div style="
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        ">
            <h2>
                Data Center Monitoring
            </h2>
            <p>
                Bonjour <strong>{username}</strong>,
            </p>
            <p>
                Un compte a été créé pour vous par un
                administrateur sur la plateforme
                Data Center Monitoring.
            </p>
            <p>
                Nom d'utilisateur : <strong>{username}</strong>
            </p>
            <p>
                Votre mot de passe temporaire est :
            </p>
            <div style="
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 2px;
                text-align: center;
                padding: 20px;
                background: #f1f5ff;
                border-radius: 8px;
            ">
                {temp_password}
            </div>
            <p>
                Connectez-vous avec ces identifiants. Il vous
                sera demandé de choisir un nouveau mot de passe
                dès votre première connexion.
            </p>
            <p>
                Si vous n'êtes pas concerné par cette création
                de compte, contactez votre administrateur.
            </p>
            <hr>
            <p style="
                color: #777;
                font-size: 12px;
            ">
                Data Center Monitoring Platform
            </p>
        </div>
    </body>
    </html>
    """
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = smtp_from
    message["To"] = recipient_email
    message.attach(
        MIMEText(
            html,
            "html"
        )
    )
    with smtplib.SMTP(
        smtp_server,
        smtp_port
    ) as server:
        server.starttls()
        server.login(
            smtp_username,
            smtp_password
        )
        server.sendmail(
            smtp_from,
            recipient_email,
            message.as_string()
        )
    return True
