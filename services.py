
from app.Modelos import modeloEstudiante as estudiante
from flask import flash
from config import db
import re
from werkzeug.security import generate_password_hash, check_password_hash
import random
import pyodbc

     
class Service:
    def __init__(self):
        self.conn = db.conn  # db.conn debe ser conexión psycopg2
        self.cursor = self.conn.cursor()

    @staticmethod
    def verificar_contrasena(stored_password, entered_password):
        if not stored_password or not entered_password:
            return False
        if not isinstance(stored_password, str):
            return False
        try:
            if stored_password.startswith(("$2a$", "$2b$", "$2y$")):
                return check_password_hash(stored_password, entered_password)
        except Exception:
            pass
        return stored_password == entered_password

    def GuardarUsuario(self, Estudiante):
        if not Estudiante:
            flash("Error: El usuario está vacío", "error")
            return False  
        try:
            select = "SELECT * FROM estudiantes WHERE correo = ?"
            correoE = Estudiante["correo"]
            self.cursor.execute(select, (correoE,))
            resultado = self.cursor.fetchone()
           
            if not resultado:
                self.cursor.execute(
                    "INSERT INTO estudiantes (nombre, correo, numeroTelefono, contrasena, Apellido) VALUES (?, ?, ?, ?, ?)",
                    (Estudiante["nombre"], Estudiante["correo"], Estudiante["numero"], Estudiante["contrasena"], Estudiante['apellido'])
                )
                self.conn.commit()
                return True
            else:
                flash("Este correo electrónico ya ha sido utilizado", "error")
                return False
        except Exception as e:
            flash(f"Error al guardar usuario: {str(e)}", "error")
            return False

    def obtenerUsuarioID(self, nombre, passw, correoE):
        try:
            print("Nombre:", nombre, "Correo:", correoE, "Pass:", passw)

            if not nombre and not passw and not correoE:
                flash("Parámetros vacíos")
                return None

            # 1. Buscar en estudiantes por correo
            selectE = "SELECT id, contrasena, rol FROM estudiantes WHERE correo = ?"
            self.cursor.execute(selectE, (correoE,))
            estudiante = self.cursor.fetchone()

            if estudiante:
                idE, hashE, rolE = estudiante
                if self.verificar_contrasena(hashE, passw):
                    return idE, rolE

            # 2. Buscar en profesores por nombre
            selectP = "SELECT id, contrasena, rol FROM profesores WHERE nombre = ?"
            self.cursor.execute(selectP, (nombre,))
            profesor = self.cursor.fetchone()

            if profesor:
                idP, hashP, rolP = profesor
                if self.verificar_contrasena(hashP, passw):
                    return idP, rolP

            # 3. Buscar en administradores por nombre
            selectA = "SELECT id_Admin, contrasena, rol FROM administradores WHERE nombre = ?"
            self.cursor.execute(selectA, (nombre,))
            admin = self.cursor.fetchone()

            if admin:
                idA, hashA, rolA = admin
                if self.verificar_contrasena(hashA, passw):
                    return idA, rolA

            # Si no se encontró el usuario o la contraseña es incorrecta
            return None

        except Exception as e:
           print(f"Error en obtenerUsuarioID: {e}")
           flash("Ocurrió un error al intentar iniciar sesión.")
           return None
            
    def  validarUsuario(self,id,rol):


              #Se consulta al Profesor
          selectProfesores="SELECT id FROM Profesores WHERE id=? AND rol=?"
          self.cursor.execute(selectProfesores, (id,rol))
          resultadoProfesor = self.cursor.fetchone()
           #Consultamos al estudiante
          selectEstudiante = "SELECT id FROM Estudiantes WHERE id= ? AND rol=?"
          self.cursor.execute(selectEstudiante, (id,rol))
          resultadoEstudiante = self.cursor.fetchone()
           #Se consulta al Administrador
          selectAdmin="SELECT id_Admin FROM Administradores WHERE id_Admin=? AND rol=?"
          self.cursor.execute(selectAdmin, (id,rol))
          resultadoAdmin=self.cursor.fetchone()
         
          if resultadoEstudiante : 
           return "E" 
                        
          elif resultadoAdmin :  
           return "A"   
  
          elif resultadoProfesor :  
            return "P" 


    # Más métodos adaptados igual:
    def Selecionarinstrumentos(self):
        try:       
            self.cursor.execute("SELECT id, nombre FROM instrumentos")
            resultados = self.cursor.fetchall()
            instrumentos = [{"id": row[0], "nombre": row[1]} for row in resultados]
            return instrumentos
        except Exception as e:
            self.conn.rollback() 
            flash(f"No se pudo ejecutar tu consulta: {str(e)}", "error")
            return []

    def guardarComprobantes(self, comprobanteRuta, estudiante_id):
        if not comprobanteRuta:
            flash("No se subió ninguna imagen")
            return False
        try:
            insert = "INSERT INTO comprobantes (comprobante, estudiante_id) VALUES (?, ?)"
            self.cursor.execute(insert, (comprobanteRuta, estudiante_id))
            self.conn.commit()
            return True
        except Exception as e:
            flash(f"Error al guardar el comprobante en la base de datos: {str(e)}", "error")
            return False   
        



    
 
    def definirCuposInstrumento(self, idInstrumento, cantidadCupos):
        query = "UPDATE instrumentos SET Cupos = ? WHERE id = ?"
        self.cursor.execute(query, (cantidadCupos, idInstrumento))
        self.conn.commit()
    
    def GetCuposInstrumentos(self, idInstrumento):
        query = "SELECT Cupos FROM instrumentos WHERE id = ?"
        self.cursor.execute(query, (idInstrumento,))
        CuposInstrumento = self.cursor.fetchone()
        if CuposInstrumento:
            return CuposInstrumento[0]
        return 0
    
    def ObtenerComprobantes(self):
        select = "SELECT id, comprobante, estudiante_id, fechaSubida, Revisado FROM comprobantes"
        self.cursor.execute(select)
        consulta = self.cursor.fetchall()
        return consulta
    
    def NombreUsuario(self, Usuario, passw):
        try:
            if not Usuario:
                return None

            print("Usuario recibido:", Usuario)
            selectE = "SELECT nombre FROM estudiantes WHERE correo = ?"
            self.cursor.execute(selectE, (Usuario,))
            estudiante = self.cursor.fetchone()

            if estudiante:
                print("Estudiante:", estudiante[0])
                return estudiante[0]

            selectP = "SELECT nombre FROM profesores WHERE nombre = ?"
            self.cursor.execute(selectP, (Usuario,))
            profesor = self.cursor.fetchone()

            if profesor:
                print("Profesor:", profesor[0])
                return profesor[0]

            selectA = "SELECT nombre FROM Administradores WHERE nombre = ?"
            self.cursor.execute(selectA, (Usuario,))
            admin = self.cursor.fetchone()

            if admin:
                print("Administrador:", admin[0])
                return admin[0]
            return None
        except Exception as e:
            self.conn.rollback()
            print("ERROR en NombreUsuario:", e)
            return None
        
    def obtenerestudiante(self, idEstudiante, correo=None):
        
        if idEstudiante:
            select = "SELECT nombre FROM estudiantes WHERE id = ?"
            self.cursor.execute(select, (idEstudiante,))
        elif correo:
            select = "SELECT nombre FROM estudiantes WHERE correo = ?"
            self.cursor.execute(select, (correo,))
        else:
            return None
    
        consulta = self.cursor.fetchone()
        print("Resultado de la consulta:", consulta)
        return consulta[0] if consulta else None
    
    def GetInstrumentoNombre(self, idInstrumento):
        select = "SELECT nombre FROM instrumentos WHERE id = ?"
        self.cursor.execute(select, (idInstrumento,))
        fila = self.cursor.fetchone()
        if fila:
            return fila[0]
        else:
            return None
    
    def UpdateInstrumentoID(self, user_id, instrumento_id):
        try:
            Update = "UPDATE estudiantes SET id_instrumentoMatr = ? WHERE id = ?"
            self.cursor.execute(Update, (instrumento_id, user_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            flash(f"Error actualizando instrumento: {str(e)}", "error")
    
    def ObtenerInstrumentoMatri(self, idE):
        select = "SELECT id_instrumentoMatr FROM estudiantes WHERE id = ?"
        self.cursor.execute(select, (idE,))
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
    def obtenerNumeroU(self, id):
        select = "SELECT numeroTelefono FROM estudiantes WHERE id = ?"
        self.cursor.execute(select, (id,))
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
    def EstudianteMatriculado(self, id):
      try:
          select = "SELECT id_instrumentoMatr FROM estudiantes WHERE id = ? "
          self.cursor.execute(select, (id,))
          consulta = self.cursor.fetchone()
          return consulta[0] if consulta else None
      except Exception as e:
          print(f"Error en EstudianteMatriculado: {e}")
          return None
    
    @staticmethod
    def validar_contrasena(password):
      if len(password) < 8:
          return "La contraseña debe tener al menos 8 caracteres"
      if not re.search(r'[A-Z]', password):
          return "Debe contener al menos una letra mayúscula"
      if not re.search(r'[a-z]', password):
          return "Debe contener al menos una letra minúscula"
      if not re.search(r'\d', password):
          return "Debe contener al menos un número"
      if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
          return "Debe contener al menos un carácter especial"
      return None
  
    def ConsultaEstudiantes(self, idInstrumento):
        print("idInstrumento recibido:", idInstrumento)
        idInstrumento_flat = [item[0] for item in idInstrumento]
        if not idInstrumento_flat:
         return []
        placeholders = ', '.join(['?'] * len(idInstrumento_flat))
        select = f"SELECT id, nombre, numeroTelefono, Apellido FROM estudiantes WHERE id_instrumentomatr IN ({placeholders})"
        self.cursor.execute(select, tuple(idInstrumento_flat))
        consulta = self.cursor.fetchall()
        return consulta
    
    def GetProfesorInstrumentos(self, idProfesor):
        select = "SELECT instrumento_id FROM instrumentos_profesores WHERE profesor_id = ?"
        self.cursor.execute(select, (idProfesor,))
        resultado = self.cursor.fetchall()
        return resultado if resultado else None
    
    def ElimiinarEstudiante(self, idEstudiante):
        update = "UPDATE estudiantes SET id_instrumentoMatr = NULL WHERE id = ?"
        resultado = self.cursor.execute(update, (idEstudiante,))
        self.conn.commit()
        return resultado
    
    def elimnarComprobante(self, idComprobante):
        delete = "DELETE FROM comprobantes WHERE id = ?"
        resultado = self.cursor.execute(delete, (idComprobante,))
        self.conn.commit()
        return resultado
   
    def VerificarCorreoUsuario(self, correoIngresado):
          select = "SELECT correo FROM estudiantes WHERE correo = ?"
          self.cursor.execute(select, (correoIngresado,))
          consulta = self.cursor.fetchone()
          return consulta
      
    @staticmethod
    def generar_codigo_aleatorio():
          return str(random.randint(100000, 999999))
      
    def actualizar_contrasena_usuario(self, Pcorreo, Pcontrasena):
          query = "UPDATE estudiantes SET contrasena = ? WHERE correo = ?"
          self.cursor.execute(query, (Pcontrasena, Pcorreo))
          self.conn.commit()
      
    def actualizar_estado_revisado(self, idComprobante, estadoNuevo):
          try:
              query = "UPDATE comprobantes SET revisado = ? WHERE id = ?"
              self.cursor.execute(query, (estadoNuevo, idComprobante))
              self.conn.commit()
          except Exception as e:
            self.conn.rollback()
            flash(f"Error actualizando estado: {e}")
    
    # Y así sucesivamente para todos los métodos...


    




       

 
     
         
                            
                        
       
        



