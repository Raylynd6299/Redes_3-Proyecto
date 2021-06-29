from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
 

 
def EnviarAlerta(Mensaje = "", ParaUsario = "", TipoAlerta = ""):
    msg = MIMEMultipart()
    message = " "
    message = Mensaje

    # setup the parameters of the message
    password = "wvnzwjmjsppudjul" #Password del correo
    msg['From'] = "raymundo.pulido.beja@gmail.com"
    msg['To'] = ParaUsario
    msg['Subject'] = TipoAlerta #Asunto del mensjae

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('74.125.192.108',587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    print ( f"Ocurrio una alerta de tipo:{TipoAlerta}") 

