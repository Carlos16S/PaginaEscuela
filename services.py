
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

    def GuardarUsuario(self, Estudiante):
        if not Estudiante:
            flash("Error: El usuario está vacío", "error")
            return False  
        try:
            select = "SELECT * FROM estudiantes WHERE correo = %s"
            correoE = Estudiante["correo"]
            self.cursor.execute(select, (correoE,))
            resultado = self.cursor.fetchone()
           
            if not resultado:
                self.cursor.execute(
                    "INSERT INTO estudiantes (nombre, correo, numeroTelefono, contrasena, Apellido) VALUES (%s, %s, %s, %s, %s)",
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
     if not nombre and not passw and not correoE:
         flash("Parámetros vacíos")
         return None
    
     # 1. Buscar en estudiantes por correo
     selectE = "SELECT id, contrasena, rol FROM estudiantes WHERE correo = %s"
     self.cursor.execute(selectE, (correoE,))
     estudiante = self.cursor.fetchone()
    
     if estudiante:
         idE, hashE, rolE = estudiante
         if check_password_hash(hashE, passw):
             return idE, rolE
    
     # 2. Buscar en profesores por nombre
     selectP = "SELECT id, contrasena, rol FROM profesores WHERE nombre = %s"
     self.cursor.execute(selectP, (nombre,))
     profesor = self.cursor.fetchone()
    
     if profesor:
         idP, hashP, rolP = profesor
         if check_password_hash(hashP, passw):
             return idP, rolP
    
     # 3. Buscar en administradores por nombre
     selectA = "SELECT id_Admin, contrasena, rol FROM administradores WHERE nombre = %s"
     self.cursor.execute(selectA, (nombre,))
     admin = self.cursor.fetchone()
    
     if admin:
         idA, hashA, rolA = admin
         if check_password_hash(hashA, passw):
             return idA, rolA
         
    def  validarUsuario(self,id,rol):
  

              #Se consulta al Profesor 
          selectProfesores="SELECT id FROM Profesores WHERE id=%s AND rol=%s"
          self.cursor.execute(selectProfesores, (id,rol))
          resultadoProfesor = self.cursor.fetchone()
           #Consultamos al estudiante
          selectEstudiante = "SELECT id FROM Estudiantes WHERE id= %s AND rol=%s"
          self.cursor.execute(selectEstudiante, (id,rol))  
          resultadoEstudiante = self.cursor.fetchone()
           #Se consulta al Administrador 
          selectAdmin="SELECT id_Admin FROM Administradores WHERE id_Admin=%s AND rol=%s"
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
            insert = "INSERT INTO comprobantes (comprobante, estudiante_id) VALUES (%s, %s)"
            self.cursor.execute(insert, (comprobanteRuta, estudiante_id))
            self.conn.commit()
            return True
        except Exception as e:
            flash(f"Error al guardar el comprobante en la base de datos: {str(e)}", "error")
            return False   
        



    
 
    def definirCuposInstrumento(self, idInstrumento, cantidadCupos):
        query = "UPDATE instrumentos SET Cupos = %s WHERE id = %s"
        self.cursor.execute(query, (cantidadCupos, idInstrumento))
        self.conn.commit()
    
    def GetCuposInstrumentos(self, idInstrumento):
        query = "SELECT Cupos FROM instrumentos WHERE id = %s"
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
          
            selectE = "SELECT nombre, contrasena FROM estudiantes WHERE correo = %s"
            self.cursor.execute(selectE, (Usuario,))
            estudiante = self.cursor.fetchone()

            if estudiante:
                nombreE, hashE = estudiante
                if check_password_hash(hashE, passw):
                    return nombreE

            
            selectP = "SELECT nombre, contrasena FROM profesores WHERE nombre = %s"
            self.cursor.execute(selectP, (Usuario,))
            profesor = self.cursor.fetchone()

            if profesor:
                nombreP, hashP = profesor
                if check_password_hash(hashP, passw):
                    return nombreP

           
            selectA = "SELECT nombre, contrasena FROM administradores WHERE nombre = %s"
            self.cursor.execute(selectA, (Usuario,))
            admin = self.cursor.fetchone()

            if admin:
                nombreA, hashA = admin
                if check_password_hash(hashA, passw):
                    return nombreA

           
            return None

        except Exception as e:
            self.conn.rollback()  
            print("ERROR en NombreUsuario:", e)
            return None
        
    def obtenerestudiante(self, idEstudiante=None, correo=None):
        if idEstudiante:
            select = "SELECT nombre FROM estudiantes WHERE id = %s"
            self.cursor.execute(select, (idEstudiante,))
        elif correo:
            select = "SELECT nombre FROM estudiantes WHERE correo = %s"
            self.cursor.execute(select, (correo,))
        else:
            return None
    
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
    def GetInstrumentoNombre(self, idInstrumento):
        select = "SELECT nombre FROM instrumentos WHERE id = %s"
        self.cursor.execute(select, (idInstrumento,))
        fila = self.cursor.fetchone()
        if fila:
            return fila[0]
        else:
            return None
    
    def UpdateInstrumentoID(self, user_id, instrumento_id):
        try:
            Update = "UPDATE estudiantes SET id_instrumentoMatr = %s WHERE id = %s"
            self.cursor.execute(Update, (instrumento_id, user_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            flash(f"Error actualizando instrumento: {str(e)}", "error")
    
    def ObtenerInstrumentoMatri(self, idE):
        select = "SELECT id_instrumentoMatr FROM estudiantes WHERE id = %s"
        self.cursor.execute(select, (idE,))
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
    def obtenerNumeroU(self, id):
        select = "SELECT numeroTelefono FROM estudiantes WHERE id = %s"
        self.cursor.execute(select, (id,))
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
    def EstudianteMatriculado(self, id):
        select = "SELECT id_instrumentoMatr FROM estudiantes WHERE id = %s"
        self.cursor.execute(select, (id,))
        consulta = self.cursor.fetchone()
        return consulta[0] if consulta else None
    
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
        idInstrumento_flat = [item[0] for item in idInstrumento]
        if not idInstrumento_flat:
         return []
        placeholders = ', '.join(['%s'] * len(idInstrumento_flat))
        select = f"SELECT id, nombre, numeroTelefono, Apellido FROM estudiantes WHERE id_instrumentomatr IN ({placeholders})"
        self.cursor.execute(select, tuple(idInstrumento_flat))
        consulta = self.cursor.fetchall()
        return consulta
    
    def GetProfesorInstrumentos(self, idProfesor):
        select = "SELECT instrumento_id FROM instrumentos_profesores WHERE profesor_id = %s"
        self.cursor.execute(select, (idProfesor,))
        resultado = self.cursor.fetchall()
        return resultado if resultado else None
    
    def ElimiinarEstudiante(self, idEstudiante):
        update = "UPDATE estudiantes SET id_instrumentoMatr = NULL WHERE id = %s"
        resultado = self.cursor.execute(update, (idEstudiante,))
        self.conn.commit()
        return resultado
    
    def elimnarComprobante(self, idComprobante):
        delete = "DELETE FROM comprobantes WHERE id = %s"
        resultado = self.cursor.execute(delete, (idComprobante,))
        self.conn.commit()
        return resultado
   
    def VerificarCorreoUsuario(self, correoIngresado):
          select = "SELECT correo FROM estudiantes WHERE correo = %s"
          self.cursor.execute(select, (correoIngresado,))
          consulta = self.cursor.fetchone()
          return consulta
      
    @staticmethod
    def generar_codigo_aleatorio():
          return str(random.randint(100000, 999999))
      
    def actualizar_contrasena_usuario(self, Pcorreo, Pcontrasena):
          query = "UPDATE estudiantes SET contrasena = %s WHERE correo = %s"
          self.cursor.execute(query, (Pcontrasena, Pcorreo))
          self.conn.commit()
      
    def actualizar_estado_revisado(self, idComprobante, estadoNuevo):
          try:
              query = "UPDATE comprobantes SET revisado = %s WHERE id = %s"
              self.cursor.execute(query, (estadoNuevo, idComprobante))
              self.conn.commit()
          except Exception as e:
            self.conn.rollback()
            flash(f"Error actualizando estado: {e}")
    
    # Y así sucesivamente para todos los métodos...


    




       

 
     
         
                            
                        
       
        



