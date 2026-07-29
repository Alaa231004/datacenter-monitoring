from database import Database


db = Database()

connection = db.connect()


if connection:
    print("Connexion réussie au serveur PostgreSQL")

    db.close(connection)

else:
    print("Connexion échouée")
