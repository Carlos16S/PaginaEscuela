##Conexión a la base de datos

import os
import psycopg2

class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                "host=dpg-d1usi3umcj7s73eqg9mg-a dbname=escuela_musica user=escu_admin password=qZRHs24K31Yjy5qmEFVtpgZnYhpYekxw port=5432"
            )
            print("✅ Conexión exitosa a PostgreSQL")
        except Exception as e:
            print("❌ Error de conexión:", e)

db = DB()








#import pyodbc
#class DB:
#    server = "CAJS2004-LAPTOP\SQLEXPRESS"
#    database = "Escuela_Musica"
#    username = "EscuAdmin"                                   #Parametros para la conexion a la base de datos
#    password = "Lopvyx82!@#"
#    driver = "ODBC Driver 17 for SQL Server"
#
#
#    def __init__(self):
#      try:
#        self.conn = pyodbc.connect(
#            f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};TrustServerCertificate=yes"
#        )
#        print("✅ Conexión exitosa a SQL Server")
#        
#      except Exception as e:
#        print("❌ Error de conexión:", e)
#
#db = DB()
        
