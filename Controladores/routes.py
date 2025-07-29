import os
from flask import Blueprint, render_template, flash,request, redirect, url_for,session,current_app
import app
from correoPass import ServicioCorreo
from services import Service 
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
main = Blueprint('main', __name__)  

sv=Service()
ce=ServicioCorreo()

@main.route('/', methods=['GET', 'POST'])  
def index():
    
      if request.method == 'POST':
        correo=request.form['email']   #AdMINPrueba
        contrasena=request.form['contrasena'] #123
        nombre=sv.NombreUsuario(Usuario=correo,passw=contrasena)
        idUsuario=sv.obtenerUsuarioID(nombre,contrasena,correoE=correo)
        if idUsuario:
          instrumento=sv.Selecionarinstrumentos()
          session['nombreU']=nombre
          session['IdU']=idUsuario[0]
          rolUsuario=idUsuario[1]
          
          validacionUsuario=sv.validarUsuario(idUsuario[0],idUsuario[1]) #Se valida el usuario
         
          if validacionUsuario=="E": 
              
               EstudianteMatri=sv.EstudianteMatriculado(session.get('IdU'))
               return render_template('SeleccionCobro.html',nombreU=nombre,EstudianteMatri=EstudianteMatri)  
          elif validacionUsuario=="P":
              
              return render_template('Cupos.html',instrumentos=instrumento)
          elif validacionUsuario=="A":
               return redirect(url_for('main.Pagos_Revisar'))
          else:
               
               return render_template('index.html')
        else: 
            mensaje="Usuario o contraseña incorrectos"
            return render_template('index.html', mensaje=mensaje)
        
       
                  
      
        
      
      return render_template('index.html')  


@main.route('/SeleccionCobro', methods=['GET', 'POST'])
def SeleccionCobro():
    
    idE=session.get('IdU')
    EstudianteMatri=sv.EstudianteMatriculado(session.get('IdU'))
    


    return render_template('SeleccionCobro.html',nombreU=session.get('nombreU'),EstudianteMatri=EstudianteMatri)# Realizar configuracion de sesiones para obtener nombre de usuario
    
   
@main.route('/cerrarSesion', methods=['GET', 'POST'])
def cerrarSesion():
    
    session.clear()

    return redirect(url_for('main.index'))
    


@main.route('/crearUsuario', methods=[ 'GET','POST'])  
def crearUsuario():
       
       
       if request.method=='POST':
           datos_usuario =                            {
           "nombre": request.form['nombre'],
           "apellido":request.form['apellido'],
           "contrasena": request.form['contrasena'],
           "numero": request.form['telefono'],
           "correo": request.form['correo']
                                                        }
           contasenaValida=sv.validar_contrasena(datos_usuario['contrasena'])
           if contasenaValida:
               flash(contasenaValida,'error')
               return render_template('crearUsuario.html',nombre=datos_usuario['nombre'],apellidos=datos_usuario['apellido'],telefono=datos_usuario['numero'],correo=datos_usuario['correo'])
           else:
             contrasenaSegura=generate_password_hash(datos_usuario['contrasena'])
             datos_usuario['contrasena']=contrasenaSegura
             usuarioGuardado=sv.GuardarUsuario(datos_usuario)
             if usuarioGuardado:
              return render_template('index.html')
             else:
                 flash('Este correo  ya esta en uso', 'error')
          
       
       return render_template('crearUsuario.html')


@main.route('/realizaPago', methods={'GET', 'POST'})
def realizaPago():
  instrumento_id = session.get('IdInstrumento')
  nombreInstrumento=sv.GetInstrumentoNombre(instrumento_id)
  if request.method=='POST':
      
      if 'imagen' not in request.files or request.files['imagen'].filename == '':
            flash('No se seleccionó ninguna imagen', 'error') 
          
            print(f"ID NUEVO  instrumento = {session.get('IdInstrumento')}")


            
            print(f"Nombre Instrumento = {nombreInstrumento}")
            return render_template('realizaPago.html', nombreInstrumento=nombreInstrumento)

      
      else:
          
         
          ComprobanteArchivo=request.files['imagen']
          filename = secure_filename(ComprobanteArchivo.filename)
        
         
         

          user_id = session.get('IdU')
          sv.UpdateInstrumentoID(user_id,session.get('IdInstrumento'))
          cupos=sv.GetCuposInstrumentos(session.get('IdInstrumento'))
          sv.definirCuposInstrumento(session.get('IdInstrumento'),cupos-1)
        
          rutaComprobante=current_app.config['Comprobantes_Ruta']
          file_path = os.path.join(rutaComprobante, filename)
          ComprobanteArchivo.save(file_path)
          ruta_relativa = f"app/static/Comprobantes_Pago/{filename}"
          sv.guardarComprobantes(ruta_relativa,session.get('IdU'))
 
          flash('Comprobante subido con exito, ', 'info')
           

       
  return  render_template('realizaPago.html',instrumento_id=session.get('IdInstrumento'),nombreInstrumento=nombreInstrumento)

@main.route('/matriculaInstrumento', methods=['GET', 'POST'])
def matriculaInstrumento():
    Cupos = None  
    instrumentos = sv.Selecionarinstrumentos()
    print("Instrumentos cargados:", instrumentos)
   
    if request.method == 'POST':
         instrumento_id = request.form.get('InstrumentoID')
         session["IdInstrumento"]=instrumento_id
     
         Cupos = sv.GetCuposInstrumentos(instrumento_id)
        
         if Cupos==0 or not Cupos :
            flash("No hay campos disponibles", 'error')
            return render_template('matriculaInstrumento.html', instrumentos=instrumentos)
        



         return redirect(url_for('main.realizaPago', InstrumentoID=instrumento_id))

    

    return render_template('matriculaInstrumento.html', instrumentos=instrumentos)


@main.route('/Cupos',methods=['GET', 'POST'])
def DefinirCupos():

   ## if request.method== 'POST':
     
     instrumento_id = request.form.get('InstrumentoID') #Guardo el id del instrumento seleccionado
     CantidadCupos = request.form.get('Cupos')
     sv.definirCuposInstrumento(instrumento_id,CantidadCupos)
     instrumento=sv.Selecionarinstrumentos()
     return render_template('Cupos.html',instrumentos=instrumento)

@main.route('/obtener_cupos/<int:instrumento_id>', methods=['GET'])
def obtener_cupos(instrumento_id):
    cupos = sv.GetCuposInstrumentos(instrumento_id)
    return {'cupos': cupos}
 

@main.route('/RevisionPagos',methods=['GET', 'POST'])
def Pagos_Revisar():
  
       comprobantes = sv.ObtenerComprobantes()
       comprobantes_con_estudiantes = []
 
       for idC,c, I,F,Revisado in comprobantes:
        idE = I  # de la  tupla se escoge el campo que tiene el id estudiante
        fecha  =F
        RevisadoC=Revisado
        estudianteN=sv.obtenerestudiante(idEstudiante=idE)
        InstrumentoE=sv.ObtenerInstrumentoMatri(idE)
        instrumentoNombre=sv.GetInstrumentoNombre(InstrumentoE)
        Usuarionumero=sv.obtenerNumeroU(idE)
        
        comprobantes_con_estudiantes.append({
        'IDC':idC,
        'comprobante': c,
        'nombre_estudiante': estudianteN,
        'Instrumento_nombre':instrumentoNombre,
        'usuariotelefono':Usuarionumero,
        'fecha':fecha,
        'Revisado':RevisadoC
        
                    })
       return render_template('RevisionPagos.html', comprobantes=comprobantes_con_estudiantes)
    

@main.route("/actualizar_comprobantes", methods=["POST"])
def actualizar_comprobantes():
    ids_revisados = request.form.getlist("revisados")  # lista de IDs marcados como revisados

    # Recorres todos los comprobantes en tu base de datos
    for item in sv.ObtenerComprobantes(): 
        id=item[0] # Suponiendo que esta función te da todos los comprobantes
        item_id = str(id)
        nuevo_estado = True if item_id in ids_revisados else False
        sv.actualizar_estado_revisado(id, nuevo_estado)  # Función que actualiza en la BD

    return redirect(url_for('main.Pagos_Revisar'))


@main.route('/ConsultaAlumnos', methods=['GET'])
def Consulta_alumnos():
    idProfesor=session.get('IdU')
  
    Instrumento_Profesor=sv.GetProfesorInstrumentos(idProfesor)
    print("ID de los instrumentos del profe",Instrumento_Profesor)
    EstudiantesMatriculado=sv.ConsultaEstudiantes(Instrumento_Profesor)
    UsuarioNombre=session.get('nombreU')

    return render_template('Alumnos.html',EstudiantesMatriculado=EstudiantesMatriculado,UsuarioNombre=UsuarioNombre)

@main.route('/EliminarAlumnos/<int:id>',methods=['POST', 'GET'])
def eliminarEstudiante(id):
      
    instrumento=sv.ObtenerInstrumentoMatri(id)
    CuposInstrumento=sv.GetCuposInstrumentos(instrumento)
    sv.definirCuposInstrumento(instrumento,CuposInstrumento+1)
    sv.ElimiinarEstudiante(id)
    return redirect(url_for('main.Consulta_alumnos'))

@main.route('/EliminarComprobante/<int:id>',methods=['POST', 'GET'])
def ElimnarComprobante(id):
    sv.elimnarComprobante(id)
    return redirect(url_for('main.Pagos_Revisar'))

@main.route('/RegresarProfesor',methods=['POST', 'GET'])
def regresarProfesor():
    return redirect(url_for('main.DefinirCupos'))

@main.route('/IntroducirCorreo',methods=['POST', 'GET'])
def IntroducirCorreo():
    if request.method== 'GET':
     return render_template('/RecuperacionCorreo.html')
   
    elif request.method=='POST':

        correo = request.form['correo']
        session['correo']=correo
        print("Correo del formulario= " ,correo)
        CorreoUser=sv.VerificarCorreoUsuario(correo)

        if not  CorreoUser:
            flash("El correo no está registrado con ningun usuario")
            return render_template('/RecuperacionCorreo.html')
        else:
            codigo = sv.generar_codigo_aleatorio()
         
            ce.enviarCorreoCodigo(correo, codigo)
            session['codigo'] = codigo
            session['correo'] = correo
            return redirect(url_for('main.VerificarCodigo'))
        
    


@main.route('/VerificarCodigo',methods=['POST', 'GET'])
def VerificarCodigo():
  if request.method=='GET':
   CorrreoUser=session.get('correo')
   return render_template('VerificacionCodigo.html',correo=CorrreoUser)
  
  elif request.method =='POST':
  
      codigo_ingresado = request.form['codigo']
      codigo_guardado=session.get('codigo')
      
      if codigo_ingresado == codigo_guardado:
         return  redirect(url_for('main.CrearNuevaContrasena'))
      else:
          flash( "Código incorrecto")
          return render_template('VerificacionCodigo.html')
 

@main.route('/CrearNuevaContrasena',methods=['POST', 'GET']) 
def CrearNuevaContrasena():  
   if request.method=='GET':
       return render_template('/ConfirmarContra.html')
   
   elif request.method =='POST':
       contrasena = request.form['contrasena']
       correo=session.get('correo')
       contasenaValida=sv.validar_contrasena(contrasena)
       if  contasenaValida:
        flash(contasenaValida,'error')
       else:
        sv.actualizar_contrasena_usuario(correo, contrasena)
        flash("Contraseña actualizada correctamente.")
        session.clear()
        return redirect(url_for('main.index'))
    
    
   return render_template('/ConfirmarContra.html')


