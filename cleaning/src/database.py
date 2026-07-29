import psycopg2
from psycopg2.extras import RealDictCursor
import os

class Database:

    def __init__(self):

    
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = os.getenv("DB_PORT", 5432)
        self.database = os.getenv("DB_NAME","datacenter_monitoring")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "msaly2310")

    def connect(self):

        try:

            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )

            print("Connexion PostgreSQL réussie.")

            return connection


        except Exception as e:

            print("Erreur de connexion PostgreSQL :")
            print(e)

            return None


    def close(self, connection):

        if connection:

            connection.close()

            print("Connexion PostgreSQL fermée.")
