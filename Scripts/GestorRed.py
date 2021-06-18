#!/usr/bin/env python3

import BackupsFTP
import SNMP
import Alertas
import os, re

__author__ = "Cortés Castillo Daniela y Pulido Bejarano Raymundo"
__copyright__ = "Copyright 2021, The R3 Project"
__credits__ = ["Cortés Castillo Daniela","Pulido Bejarano Raymundo"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Cortés Castillo Daniela y Pulido Bejarano Raymundo"
__email__ = "rayescomed@gmail.com"
__status__ = "Production"

ips_routers = None
routers = None
Servidores = {"Servidor_1":[["DHCP","FTP","SSH","SNMP_A"],"192.168.226.18"],"Servidor_2":[["SNMP_NMS","SSH","FTP"],"192.168.226.34"],"Servidor_3":[["DNS","SSH","FTP","SNMP_A"],"192.168.226.26"] }
SNMPServidores = [SNMP.Snmp(nombreDevice="Servidor 1", userName="R3SNMP",destHost="192.168.226.18",protAuth="SHA-256",passAuth="RaDa22962"),SNMP.Snmp(nombreDevice="Servidor 2", userName="R3SNMP",destHost="192.168.226.26",protAuth="SHA-256",passAuth="RaDa22962")]
SNMPRouters = None


def Menu():
    print("-----------------------------------------------------------------------------------------------------------------")
    print(
        """
       oooooooooo.   o8o                                                           o8o        .o8            
       `888'   `Y8b  `"'                                                           `"'       "888            
        888     888 oooo   .ooooo.  ooo. .oo.   oooo    ooo  .ooooo.  ooo. .oo.   oooo   .oooo888   .ooooo.  
        888oooo888' `888  d88' `88b `888P"Y88b   `88.  .8'  d88' `88b `888P"Y88b  `888  d88' `888  d88' `88b 
        888    `88b  888  888ooo888  888   888    `88..8'   888ooo888  888   888   888  888   888  888   888 
        888    .88P  888  888    .o  888   888     `888'    888    .o  888   888   888  888   888  888   888 
       o888bood8P'  o888o `Y8bod8P' o888o o888o     `8'     `Y8bod8P' o888o o888o o888o `Y8bod88P" `Y8bod8P'                                                                                        
        """)
    print("Opciones:                                                  ")
    print("     1) Realizar Backup de todos los routers               ")    #Ready
    print("     2) Realizar Backup de un router                       ")    #Ready
    print("     3) Restaurar un router                                ")    #Ready
    print("     4) Listar Routers de la Red                           ")    #Ready
    print("     5) IP Host                                            ")    #Ready
    print("     6) Listar servidores y servicios                      ")    #Ready
    print("     7) Listar versiones de Backups                        ")    #Ready 
    print("     8) Borrar Backup                                      ")    #Ready 
    print("     9) Listar Ip y mascara de interfaces de un router     ")    #Ready
    print("    10) Comprobar que las interfaces esten activas         ")    #Ready
    print("    11) Comprobar conectividad de Routers y servidores     ")    #Ready
    print("    12) Cambiar destino de alertas                         ")    #Ready
    print("    13) Salir                                              ")    #Ready
    print("-----------------------------------------------------------------------------------------------------------------")
    
def Opcion1():
    global ips_routers

    print("Realizando Backups de todos los routers")

    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    for ip in ips_routers:
        BackupsFTP.obtener_backup(ip)
    BackupsFTP.mover_backups()

    print("Backups Realizados !!!")

def Opcion2():
    global ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    
    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del router al que se le realizara un Backup: ")

    if routers.get(IDRouter) :
        print(f"Realizando el Back up al Router {IDRouter} IP:{routers[IDRouter]}")
        BackupsFTP.obtener_backup(routers[IDRouter])
        BackupsFTP.mover_backups()
        print("Backup Realizado !!!")
    else:
        print(f"No existe el Router designado")

def Opcion3():
    global ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)

    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del router que va a restaurar: ")
    if routers.get(IDRouter) :
        backs_F = BackupsFTP.list_backs_router(IDRouter)
        if backs_F: 
            print(f"Los backups del router {IDRouter} son:")
            for ind,backup in enumerate(backs_F):
                print(f"    {ind}) {backup}")
            try:
                NameBack = int(input("Ingrese el numero del backup:") )
                if 0 > NameBack > len(backs_F):
                    print("Error la opcion no es valida,fuera de rango")
            except:
                print("Error la opcion no es valida")
            print(f"Realizando la restauracion del router {IDRouter} con el backup: {backs_F[NameBack]}")
            BackupsFTP.SubirRespaldoRouter(routers[IDRouter],backs_F[NameBack])
        else:
            print(f"No Hay Backups del router {IDRouter}")
    else:
        print(f"No existe el Router designado")

def Opcion4():
    global ips_routers, routers

    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

def Opcion5():
    print(f"La ip de la pc local es: {BackupsFTP.obtener_ip_host()}")

def Opcion6():
    global Servidores
    print("Los servidores de la Red son:")
    for servidor in Servidores.keys():
        print(f"{servidor}:")
        print(f"    Servicios:")
        for service in Servidores[servidor][0]:
            print(f"            {service}")
        print(f"    Ip:  {Servidores[servidor][1] }")

def Opcion7():
    global ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)

    for router in routers.keys():
        backs_F = BackupsFTP.list_backs_router(router)
        if backs_F: 
            print(f"Los backups del router {router} son:")
            for ind,backup in enumerate(backs_F):
                print(f"    {ind}) {backup}")
        else:
            print(f"El router {router} no tiene backups guardados")

def Opcion8():
    global ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)

    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del router del que eliminara el backup: ")
    if routers.get(IDRouter) :
        backs_F = BackupsFTP.list_backs_router(IDRouter)
        if backs_F: 
            print(f"Los backups del router {IDRouter} son:")
            for ind,backup in enumerate(backs_F):
                print(f"    {ind}) {backup}")
            try:
                NameBack = int(input("Ingrese el numero del backup:") )
                if 0 > NameBack > len(backs_F):
                    print("Error la opcion no es valida,fuera de rango")
            except:
                print("Error la opcion no es valida")
            
            res = BackupsFTP.BorrarBackup(backs_F[NameBack])
            if res:
                print(f"Backup: {backs_F[NameBack]}  eliminado !!")
            else:
                print("Error al eliminar el backup")
        else:
            print(f"No Hay Backups del router {IDRouter}")
    else:
        print(f"No existe el Router designado")

def Opcion9():
    global SNMPRouters, ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    if SNMPRouters == None:
        SNMPRouters = list()
        for router in routers.keys():
            SNMPRouters.append( SNMP.Snmp(nombreDevice=router , userName="R3SNMP",destHost=routers[router],protAuth="SHA",passAuth="RaDa22962") )


    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del Router que desea consultar: ")    
    if routers.get(IDRouter) :
        for SNMPRouter in SNMPRouters:
            if SNMPRouter.NombreDevice == IDRouter:
                print(f"Obteniendo informacion del Router {IDRouter}")
                res = SNMP.InfoIntRouter(SNMPRouter)
                if res :
                    print("Se obtuvo la informacion del router correctamente")
                elif res == False:
                    print(f"Error al obtener informacion del router {IDRouter}")
                break                
    else:
        print(f"No existe el Router designado")

def Opcion10():
    global SNMPRouters, ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    if SNMPRouters == None:
        SNMPRouters = list()
        for router in routers.keys():
            SNMPRouters.append( SNMP.Snmp(nombreDevice=router , userName="R3SNMP",destHost=routers[router],protAuth="SHA",passAuth="RaDa22962") )


    print("Los Router de la topologia son: ")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del Router que desea consultar: ")    
    if routers.get(IDRouter) :
        for SNMPRouter in SNMPRouters:
            if SNMPRouter.NombreDevice == IDRouter:
                print(f"Obteniendo informacion del Router {IDRouter}")
                res = SNMP.InfoActividadRouter(SNMPRouter)
                if res :
                    print("Se obtuvo la informacion del router correctamente")
                elif res == False:
                    print(f"Error al obtener informacion del router {IDRouter}")
                break                
    else:
        print(f"No existe el Router designado")

def Opcion11():
    global SNMPRouters, ips_routers, routers, SNMPServidores
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    if SNMPRouters == None:
        SNMPRouters = list()
        for router in routers.keys():
            SNMPRouters.append( SNMP.Snmp(nombreDevice=router , userName="R3SNMP",destHost=routers[router],protAuth="SHA",passAuth="RaDa22962") )

    for SNMPServidor in  SNMPServidores:
        info_S = SNMPServidor.getSNMP()
        if info_S:
            print(f"El {SNMPServidor.NombreDevice} : {SNMPServidor.DestHost} se encuentra activo ")
        else:
            print(f"El {SNMPServidor.NombreDevice} esta inactivo")
    
    for SNMPRouter in SNMPRouters:
        info_R = SNMPRouter.getSNMP("sysName")
        if info_R:
            print(f"El {SNMPRouter.NombreDevice} : {SNMPRouter.DestHost} se encuentra activo ")
        else:
            print(f"El {SNMPRouter.NombreDevice} esta inactivo")

def Opcion12():
    with open("/home/warning.config","a+") as EmailFile:
        EmailFile.seek(0,0)
        email = EmailFile.read().strip()
    if email == "":
        emailNew = input("Ingrese el email al que se enviaran las alertas:  ")
    else:
        print(f"El email al que se envian las advertencias actualmente es: {email}")
        emailNew = input("Ingrese el email al que se enviaran las alertas:  ")

    if emailNew:
        res = re.search(r"[a-zA-Z0-9\._]+@[a-zA-Z\.]+\.[a-zA-Z]+",emailNew)
        
        if res == None:
            print("Error la cadena ingresada no es un email")
        else:
            with open("/home/warning.config","w") as EmailFile:
                EmailFile.write(emailNew)
            print("Email modificado con exito")
    else:
        print("Error al recibir el email")

if __name__ == "__main__":
    os.popen(f"mkdir -p ~/Backups")

    with open("/home/warning.config","a+") as EmailFile:
        EmailFile.seek(0,0)
        email = EmailFile.read().strip()
    if email == "":
        emailNew = input("Ingrese el email al que se enviaran las alertas:  ")
        res = re.search(r"[a-zA-Z0-9\._]+@[a-zA-Z\.]+\.[a-zA-Z]+",emailNew)
        if res == None:
            print("Error la cadena ingresada no es un email")
        else:
            with open("/home/warning.config","w") as EmailFile:
                EmailFile.write(emailNew)
            print("Email registrado con exito")
            email = emailNew
    else:
        print(f"El email al que se envian las advertencias actualmente es: {email}")
    
   

    while(True):
        opcion = 0
        os.system("clear")
        print(f"El email al que se envian las advertencias es: {email} !!")
        Menu()
        try:
            opcion = int(input("Ingrese la opcion deseada: "))
        except :
            print("Error al recibir la opcion seleccionada")
        
        if 1 < opcion > 13:
            print("Opcion invalida")
        if opcion == 1:
            Opcion1()
        elif opcion == 2:
            Opcion2()
        elif opcion == 3:
            Opcion3()
        elif opcion == 4:
            Opcion4()
        elif opcion == 5:
            Opcion5()
        elif opcion == 6:
            Opcion6()
        elif opcion == 7:
            Opcion7()
        elif opcion == 8:
            Opcion8()
        elif opcion == 9:
            Opcion9()
        elif opcion == 10:
            Opcion10()
        elif opcion == 11:
            Opcion11()
        elif opcion == 12:
            Opcion12()    
        elif opcion == 13:
            break

        try:
            Op = int(input("Continuar si->1 no->0  :  "))
            if Op != 1:
                break
        except:
            print("Opcion invalida")
        opcion = 0
