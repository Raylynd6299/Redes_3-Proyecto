#!/usr/bin/env python3
import os,re,time
import telnetlib

def list_backs_router(RouterID):
    path_back = "~/Backups/"
    backs = os.popen(f"ls {path_back}{RouterID}").read()
    if backs :
        backs = backs.strip().split("\n")
    else:
        backs = None
    return backs

def SubirRespaldoRouter(ipRouter, NomBack):
    if NomBack == "" or ipRouter == "":
        return None

    path_back = "~/Backups/"
    path_ftp = "/home/Uftp/"
    
    RouterNum = NomBack.strip().split("-")[0]

    os.popen(f"mv {path_back}{RouterNum}/{NomBack} {path_ftp}").read()

    password = "RD226"
    passwd_2 = "RD226"
    addr_host = obtener_ip_host()
    
    #Creamos la coneccion Telnet
    tn = telnetlib.Telnet(ipRouter)

    #LLevamos a cabo la comunicacion como si fuera en la tty o terminal 
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.read_until(b"Password: ")
    tn.write(passwd_2.encode('ascii') + b"\n")
    #Con este comando creamos una copy de la configuracion y la enviamos via ftp   
    tn.write(b"copy ftp: running-config \n")
    #Despues nos pide a que host y le mandamos la direccion
    tn.write(addr_host.encode('ascii') + b"\n")
    #le confirmamos el nombre por defecto con  un enter o \n
    tn.write(NomBack.encode('ascii')+ b"\n")
    tn.write(b"\n")
    #terminamos la coneccion
    tn.write(b"exit\n")
    #leemos todo para que se efectue las operaciones y mostremos la salida
    Resultado = tn.read_all().decode('ascii')
    
    if "bytes copied" in Resultado:
        print(f"El router {RouterNum} fue restaurado correctamente")
    else:
        print(f"Error al restaurar el router {RouterNum}")

    os.popen(f"mv {path_ftp}{NomBack} {path_back}{RouterNum}").read()

def Obtener_ID_Router(ips_routers):
    Routers = dict()
    for ip in ips_routers:

        password = "RD226"    
        #Creamos la coneccion Telnet
        tn = telnetlib.Telnet(ip)

        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        RouterID = tn.read_until(b">").decode('ascii')
        RouterID = RouterID.strip().replace(">","")
        tn.write(b"exit\n")
        tn.read_all().decode('ascii')

        Routers[RouterID] = ip
    return Routers

def obtener_ips_routers(): 

    """ Esta funcion obtendra las ips de los router mediante 
    la tabla de ruteo del router de salida """

    ip_local = obtener_ip_host()
    ip_local = ip_local.split(".")
    ip_local[-1] = str(int(ip_local[-1])-1)
    ip_local_Router = ".".join(ip_local)
    
    password = "RD226"    
    
    #Creamos la coneccion Telnet
    tn = telnetlib.Telnet(ip_local_Router)

    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"sh ip ro\n ")
    tn.write(b"exit\n")
    tab_routeo = tn.read_all().decode('ascii')

    ips_routers = []
    ips = re.findall(r"[1-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]{1,2}",tab_routeo)
    for ip in ips:
        if( int(ip.strip().split("/")[-1]) == 30 or int(ip.strip().split(".")[-1].split("/")[0]) == 40 ):
            ip_aux = ip.split("/")[0].split(".")
            ip_aux[-1] = str( int( ip_aux[-1] ) + 2 )
            ip_aux = ".".join(ip_aux)
            ips_routers.append(ip_aux)

    ip_aux = ips_routers[-1].split(".")
    ip_aux[-1] = str( int( ip_aux[-1] ) -1 )
    ips_routers.append(".".join(ip_aux))

    return ips_routers

def obtener_ip_host():
    """ Obtenemos la ip del host conectada a GNS3 """

    ip_local = os.popen("hostname -I").read()
    ip_host = ip_local.strip().split(" ")[0]
    
    return ip_host

def obtener_backup(ip):
    """Funcion con la que se obtiene cada uno de los backups

    ip => es la ip de gateway de la subred.

    password => Es la contraseña para acceder a los routers por telnet,
                esta fue configurada por el administrador de la red.

    passwd_1 => Es la contraseña para acceder a la configuracion en el router

    add_host => Es la direccion del host donde se guardara la configuracion
     
    """
        
    password = "RD226"
    passwd_2 = "RD226"
    addr_host = obtener_ip_host()
    
    #Creamos la coneccion Telnet
    tn = telnetlib.Telnet(ip)

    #LLevamos a cabo la comunicacion como si fuera en la tty o terminal 
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.read_until(b"Password: ")
    tn.write(passwd_2.encode('ascii') + b"\n")
    #Con este comando creamos una copy de la configuracion y la enviamos via ftp
    
    RouterNum = tn.read_until(b"#").decode('ascii')
    RouterNum = RouterNum.strip().replace("#","")
    os.popen(f"mkdir -p ~/Backups/{RouterNum}")
    FyH = f"{ time.strftime('%d-%m-%y') }_{time.strftime('%H-%M-%S')}"

    tn.write(b"copy running-config ftp: \n")
    #Despues nos pide a que host y le mandamos la direccion
    tn.write(addr_host.encode('ascii') + b"\n")
    #le confirmamos el nombre por defecto con  un enter o \n
    tn.write(RouterNum.encode('ascii')+b"-config-"+ FyH.encode('ascii') + b"\n")
    #terminamos la coneccion
    tn.write(b"exit\n")
    #leemos todo para que se efectue las operaciones y mostremos la salida
    Resultado = tn.read_all().decode('ascii')
    
    if "bytes copied" in Resultado:
        print(f"El router {RouterNum} realizo el Backup correctamente")
    else:
        print(f"Error al realizar el Backup del router {RouterNum}")

def mover_backups():

    """ Esta funcion esta diseñada para mover los archivos de configuracion
    a la carpeta destino de backups 
     
    path_ftp => contiene el path o direccion donde se alojan los datos traidos por ftp

    path_backs => Es el path donde se guardara los backups
    """

    path_ftp = "/home/Uftp/"
    path_backs = "~/Backups/"

    NameBackups = os.popen("ls " + path_ftp ).read()
    NameBackups = NameBackups.strip().split("\n")

    #Este ciclo movera cada archivo de configuracion a su respectiva carpeta a la vez que crea estas
    for back in NameBackups:
        NumRo = back.strip().split("-")[0]
        os.popen(f"mv {path_ftp}{back} {path_backs}{NumRo}")

