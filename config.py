##Conexión a la base de datos

import os
import psycopg2
import pyodbc

class DB:
    def __init__(self):
        try:
            self.conn = pyodbc.connect(
             #   "host=dpg-d1usi3umcj7s73eqg9mg-a dbname=escuela_musica user=escu_admin password=qZRHs24K31Yjy5qmEFVtpgZnYhpYekxw port=5432"
             "DRIVER={ODBC Driver 17 for SQL Server};"
             "SERVER=CAJS2004-LAPTOP;"
             "DATABASE=Escuela_Musica;"
             "UID=EscuAdmin;"
             "PWD=Lopvyx82!@#;"
             "TrustServerCertificate=yes;"
            )
            print("✅ Conexión exitosa a PostgreSQL")
        except Exception as e:
            print("❌ Error de conexión:", e)

db = DB()







