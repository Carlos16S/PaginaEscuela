import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ServicioCorreo:
    def enviarCorreoCodigo(self, correo_destino, codigo):
        # Configuración del correo del remitente
        remitente = "escuelamusicaalvarado@gmail.com"
        clave = "alhq ozll ebfh jciy"

        # Configuración del mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = correo_destino
        mensaje['Subject'] = "Código de verificación"
        
        cuerpo = f"Tu código de verificación es: {codigo}, no comparta este código con terceros"
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        try:
            # Conexión con el servidor SMTP de Gmail
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, clave)
            servidor.send_message(mensaje)
            servidor.quit()
            print("Correo enviado correctamente.")
        except Exception as e:
            print("Error al enviar el correo:", e)
