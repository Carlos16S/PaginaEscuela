##Conexión a la base de datos

import pyodbc
class DB:
    server = "CAJS2004-LAPTOP\SQLEXPRESS"
    database = "Escuela_Musica"
    username = "EscuAdmin"                                   #Parametros para la conexion a la base de datos
    password = "Lopvyx82!@#"
    driver = "ODBC Driver 17 for SQL Server"


    def __init__(self):
      try:
        self.conn = pyodbc.connect(
            f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};TrustServerCertificate=yes"
        )
        print("✅ Conexión exitosa a SQL Server")
        
      except Exception as e:
        print("❌ Error de conexión:", e)

db = DB()
        
