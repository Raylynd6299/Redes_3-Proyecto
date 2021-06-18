#!/usr/bin/env python3

import BackupsFTP
import SNMP
import Alertas
import os
import threading


SNMPServidores = [SNMP.Snmp(nombreDevice="Servidor 1", userName="R3SNMP",destHost="192.168.226.18",protAuth="SHA-256",passAuth="RaDa22962"),SNMP.Snmp(nombreDevice="Servidor 2", userName="R3SNMP",destHost="192.168.226.26",protAuth="SHA-256",passAuth="RaDa22962")]
SNMPRouters = None
ips_routers = None
routers = None
Email = ""

def Demonio(**Objetivos):
    for obj in Objetivos.keys():
        print(f"{obj.NombreDevice}:{obj.DestHost}")


def main():
    global SNMPRouters, SNMPServidores, ips_routers, routers, Email
    
    ips_routers = BackupsFTP.obtener_ips_routers()
    routers = BackupsFTP.Obtener_ID_Router(ips_routers)
    SNMPRouters = list()
    for router in routers.keys():
        SNMPRouters.append( SNMP.Snmp(nombreDevice=router , userName="R3SNMP",destHost=routers[router],protAuth="SHA",passAuth="RaDa22962") )
    email = ""
    while email == "":
        with open("/home/warning.config","a+") as EmailFile:
            EmailFile.seek(0,0)
            email = EmailFile.read().strip()
    Email = email

    NUM_T = 3
    Hilos = []
    Hilos.append(threading.Thread(      target=Demonio,
                                        kwargs={
                                                SNMPServidores[0].NombreDevice:SNMPServidores[0],
                                                SNMPServidores[1].NombreDevice:SNMPServidores[1]
                                                }
                                 ))
    for num_T in range(NUM_T):
        Hilos.append(threading.Thread(  target=Demonio,
                                        kwargs={
                                                SNMPRouters[num_T*2].NombreDevice:SNMPRouters[num_T*2],
                                                SNMPRouters[(num_T*2)+1].NombreDevice:SNMPRouters[(num_T*2)+1]
                                                }
                                    ))
    for h in Hilos:    
        h.start()
        
if __name__ == "__name__":
    main()