#!/usr/bin/env python3

import BackupsFTP
import SNMP
import Alertas
import os

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
Servidores = {"Servidor_1":[["DHCP","FTP","SSH","SNMP_A"],"192.168.226.18"],"Servidor_3":[["DNS","SSH","FTP","SNMP_A"],"192.168.226.26"],"Servidor_2":[["SNMP_NMS","SSH","FTP"],"192.168.226.34"] }

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
    print("     3) Restaurar un router con backup                     ")    #Ready
    print("     4) Listar Routers de la Red                           ")    #Ready
    print("     5) IP Host                                            ")    #Ready
    print("     6) Listar servidores y servicios                      ")    #Ready
    print("     7) Listar versiones de Backups                        ")    #Ready 
    print("     8) Listar Ip y mascara de interfaces de un router     ") #listar interfaces de un router( interfaz ip mask activo)
    print("     9) Comprobar que las interfaces esten activas         ")
    print("    10) Comprobar conectividad de Routers y servidores     ")
    print("    11) Cambiar destino de alertas                         ") #Agregar identificar Routers y obtener ip de routers, 
    print("    12) Salir                                              ")
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
    
    print("Los Router de la topologia son: \n")
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

    print("Los Router de la topologia son: \n")
    for router in routers.keys():
        print(f"    Router: {router}, IP:{routers[router]}")

    IDRouter = input("Ingrese el identificador del router que va a restaurar: ")
    if routers.get(IDRouter) :
        backs_F = BackupsFTP.list_backs_roruter(IDRouter)
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
    print("Los Router de la topologia son: \n")
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
            print(f"        {service}")
        print(f"Ip:{Servidores[servidor][1] }")

def Opcion7():
    global ips_routers, routers
    
    if ips_routers == None:
        ips_routers = BackupsFTP.obtener_ips_routers()
    if routers == None:
        routers = BackupsFTP.Obtener_ID_Router(ips_routers)

    for router in routers.keys():
        backs_F = BackupsFTP.list_backs_roruter(router)
        if backs_F: 
            print(f"Los backups del router {router} son:")
            for ind,backup in enumerate(backs_F):
                print(f"    {ind}) {backup}")
        else:
            print(f"El router {router} no tiene backups guardados")


if __name__ == "__main__":
    os.popen(f"mkdir -p ~/Backups")

    Menu()
    try:
        opcion = int(input("Ingrese la opcion deseada: "))
    except :
        print("Error al recibir la opcion seleccionada")
    
    if 1 < opcion > 12:
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

    # SNMP.prueba()
    # BackupsFTP.prueba()

# if __name__ == "__main__":
#     
#     ips_routers = obtener_ips_routers()
#     routers = Obtener_ID_Router(ips_routers)
    
#     print("Los Router de la topologia son: \n")

#     for router in routers.keys():
#         print(f"Router: {router}, IP:{routers[router]}")
    
#     IDRouter = input("Ingrese el identificador del router que va a restaurar: ")
#     if routers.get(IDRouter) :
#         backs_F = list_backs_roruter(IDRouter)
#         if backs_F: 
#             print(f"Los backups del router {IDRouter} son:")
#             print(backs_F)
#             NameBack = input("Ingrese el nombre del backup:")
#             if NameBack in backs_F:
#                 SubirRespaldoRouter(routers[IDRouter],NameBack)
#             else:
#                 print("Archivo no encontrado")
#         else:
#             print(f"No Hay Backups del {IDRouter}")
#     else:
#         print(f"No existe el Router designado")
    

#     #print(routers)
#     # for ip in ips_routers:
#     #     obtener_backup(ip)
#     # mover_backups()


# def main():
#     Servidor_1 = Snmp(nombreDevice="Servidor 1", userName="R3SNMP",destHost="192.168.226.18",protAuth="SHA-256",passAuth="RaDa22962")
#     Servidor_2 = Snmp(nombreDevice="Servidor 2", userName="R3SNMP",destHost="192.168.226.26",protAuth="SHA-256",passAuth="RaDa22962")
#     Router_1 = Snmp(nombreDevice="Router 1", userName="R3SNMP",destHost="192.168.226.49",protAuth="SHA",passAuth="RaDa22962")
#     Router_2 = Snmp(nombreDevice="Router 2", userName="R3SNMP",destHost="192.168.226.50",protAuth="SHA",passAuth="RaDa22962")
#     Router_3 = Snmp(nombreDevice="Router 3", userName="R3SNMP",destHost="192.168.226.54",protAuth="SHA",passAuth="RaDa22962")
#     Router_4 = Snmp(nombreDevice="Router 4", userName="R3SNMP",destHost="192.168.226.58",protAuth="SHA",passAuth="RaDa22962")
#     Router_5 = Snmp(nombreDevice="Router 5", userName="R3SNMP",destHost="192.168.226.33",protAuth="SHA",passAuth="RaDa22962")
#     Router_6 = Snmp(nombreDevice="Router 6", userName="R3SNMP",destHost="192.168.226.42",protAuth="SHA",passAuth="RaDa22962")

#     infoS1 = Servidor_1.getSNMP(DESCR_OID)
#     infoS2 = Servidor_2.getSNMP(DESCR_OID)
#     infoR1 = Router_1.getSNMP(DESCR_OID)
#     infoR2 = Router_2.getSNMP(DESCR_OID)
#     infoR3 = Router_3.getSNMP(DESCR_OID)
#     infoR4 = Router_4.getSNMP(DESCR_OID)
#     infoR5 = Router_5.getSNMP(DESCR_OID)
#     infoR6 = Router_6.getSNMP(DESCR_OID)
    
#     print(f"La informacion del {Servidor_1.NombreDevice} es:\n {infoS1}")
#     print(f"La informacion del {Servidor_2.NombreDevice} es:\n {infoS2}")
#     print(f"La informacion del { Router_1.NombreDevice } es:\n {infoR1}")
#     print(f"La informacion del { Router_2.NombreDevice } es:\n {infoR2}")
#     print(f"La informacion del { Router_3.NombreDevice } es:\n {infoR3}")
#     print(f"La informacion del { Router_4.NombreDevice } es:\n {infoR4}")
#     print(f"La informacion del { Router_5.NombreDevice } es:\n {infoR5}")
#     print(f"La informacion del { Router_6.NombreDevice } es:\n {infoR6}")

# if __name__ == "__main__":
#     main()
