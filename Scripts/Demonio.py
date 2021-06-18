#!/usr/bin/env python3

import BackupsFTP
import SNMP
import Alertas
import time
import threading

cpmCPUTotal1minRev = ".1.3.6.1.4.1.9.9.109.1.1.1.1.7" #  0 >= V <= 100 porcentual
cpmCPUTotal5secRev = ".1.3.6.1.4.1.9.9.109.1.1.1.1.6"

SNMPServidores = [SNMP.Snmp(nombreDevice="Servidor 1", userName="R3SNMP",destHost="192.168.226.18",protAuth="SHA-256",passAuth="RaDa22962"),SNMP.Snmp(nombreDevice="Servidor 2", userName="R3SNMP",destHost="192.168.226.26",protAuth="SHA-256",passAuth="RaDa22962")]
SNMPRouters = None
ips_routers = None
routers = None
Email = ""

def Demonio_R(**Objetivos):
    global Email,cpmCPUTotal1minRev

    # El estatus de up o dowm
    ifAdminstatus = {}
    # Las ip directamente conectadas
    ipAdEntAddr   = {}  
    #Numero de eventos fallidos
    mteEventFailures = []
    # Si los saltos de ruteo estan active
    ipCidrRouteStatus = {}
    # packetes que antenido error dentro de ellos
    ifInErrors = {}
    #Numero de datagramas descartados por error ip destino     
    ipInAddrErrors = []  
    #Errores de entrada ICMP     
    icmpInErrors = []
    #Errores de entrada TCP checksum
    tcpInErrs = []
    #Errores de entrada UDP 
    udpInErrs = []
    #Pocentaje de uso del CPU
    cpmCPUTotal1minRev_Count = []

    limpiar = lambda info: [ linea.strip().split(" ")[3]  for linea in (info.strip().split("\n")) ]

    # for obj in Objetivos.keys():
    #     print(f"{obj}:{Objetivos[obj].DestHost}") 
    while (True):

        if not ifAdminstatus:
            for obj in Objetivos.keys():
                EstadoInicialINT = Objetivos[obj].walkSNMP("ifAdminstatus")
                ifAdminstatus[Objetivos[obj].NombreDevice] = limpiar(EstadoInicialINT)
        else:
            for obj in Objetivos.keys():
                EstadoInicialINT = Objetivos[obj].walkSNMP("ifAdminstatus")
                estados = limpiar(EstadoInicialINT)
                for interfaceEST in range(len(estados)):
                    if estados[interfaceEST] != ifAdminstatus[Objetivos[obj].NombreDevice][interfaceEST] :
                        if "up" in ifAdminstatus[Objetivos[obj].NombreDevice][interfaceEST]:
                            NameInt = Objetivos[obj].getSNMP(f"ifDescr.{interfaceEST+1}")
                            NameInt = NameInt.strip().split(" ")[3]
                            Alertas.EnviarAlerta(f"La interface {NameInt} se acaba de caer en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de Interface")  
                        ifAdminstatus[Objetivos[obj].NombreDevice][interfaceEST] = estados[interfaceEST]
        
        if not ipAdEntAddr:
            for obj in Objetivos.keys():
                ipsRou = Objetivos[obj].walkSNMP("ipAdEntAddr")
                ipAdEntAddr[Objetivos[obj].NombreDevice] = limpiar(ipsRou)
        else:
            for obj in Objetivos.keys():
                ipsRou = Objetivos[obj].walkSNMP("ipAdEntAddr")
                ipsR = limpiar(ipsRou)
                if len(ipAdEntAddr[Objetivos[obj].NombreDevice]) == len(ipsR):
                    for ip in range(len(ipsR)):
                        if ipsR[ip] != ipAdEntAddr[Objetivos[obj].NombreDevice][ip] :
                            Alertas.EnviarAlerta(f"La ip {ipAdEntAddr[Objetivos[obj].NombreDevice][ip]} cambio a {ipsR[ip]} en el router {Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"cambio de ip en router")  
                            ipAdEntAddr[Objetivos[obj].NombreDevice][ip] = ipsR[ip]
                else:
                    numIP = 0
                    diferentes = []
                    for ip in ipsR:
                        if ip in ipAdEntAddr[Objetivos[obj].NombreDevice]:
                            numIP += 1
                        else:
                            diferentes.append(ip)
                    if numIP == len(ipAdEntAddr[Objetivos[obj].NombreDevice]): # Se agregaron ips
                        mensaje = f"Se agregaron las siguientes ips al router {Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}: \n"
                        for nueva in diferentes:
                            mensaje += f"       {nueva} \n"
                            Alertas.EnviarAlerta(mensaje,Email,"Se agregaron ips en router")  
                    elif numIP < len(ipAdEntAddr[Objetivos[obj].NombreDevice]): # Se eliminaron ips
                        mensaje = f"Se eliminaron ips al router {Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost} y se agregaron: \n"
                        for nueva in diferentes:
                            mensaje += f"       {nueva} \n"
                            Alertas.EnviarAlerta(mensaje,Email,"Se eliminaron ips existentes en router")  
        
        if not mteEventFailures :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("mteEventFailures.0")
                if erroresmte:
                    mteEventFailures.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    mteEventFailures.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("mteEventFailures.0")
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if mteEventFailures[indice] < errorAct:
                        Alertas.EnviarAlerta(f"Se error en evento del router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"error de evento")  
                        mteEventFailures[indice] = errorAct
                        indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        if not ipCidrRouteStatus:
            for obj in Objetivos.keys():
                estadosTR = Objetivos[obj].walkSNMP("ipCidrRouteStatus")
                ipCidrRouteStatus[Objetivos[obj].NombreDevice] = limpiar(estadosTR)
        else:
            for obj in Objetivos.keys():
                estadosTR = Objetivos[obj].walkSNMP("ipCidrRouteStatus")
                estados = limpiar(estadosTR)
                for interfaceEST in range(len(estados)):
                    if estados[interfaceEST] != ipCidrRouteStatus[Objetivos[obj].NombreDevice][interfaceEST] :
                        if "active" in ipCidrRouteStatus[Objetivos[obj].NombreDevice][interfaceEST]:
                            NameInt = Objetivos[obj].getSNMP(f"ipCidrRouteStatus.{interfaceEST+1}")
                            NameInt = NameInt.strip()
                            Alertas.EnviarAlerta(f"Se acaba de caer la conexion en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}\n conexion perdida es {NameInt}",Email,"Caida de coneccion")  
                        ipCidrRouteStatus[Objetivos[obj].NombreDevice][interfaceEST] = estados[interfaceEST]

        if not ifInErrors:
            for obj in Objetivos.keys():
                EstadoInicialINT = Objetivos[obj].walkSNMP("ifInErrors")
                ifInErrors[Objetivos[obj].NombreDevice] = limpiar(EstadoInicialINT)
        else:
            for obj in Objetivos.keys():
                EstadoInicialINT = Objetivos[obj].walkSNMP("ifInErrors")
                estados = limpiar(EstadoInicialINT)
                for interfaceEST in range(len(estados)):
                    if estados[interfaceEST] != ifInErrors[Objetivos[obj].NombreDevice][interfaceEST] :
                        if int(estados[interfaceEST]) > 255:
                            NameInt = Objetivos[obj].getSNMP(f"ifDescr.{interfaceEST+1}")
                            NameInt = NameInt.strip().split(" ")[3]
                            Alertas.EnviarAlerta(f"La interface {NameInt} ah recibido mas de 255 errores en el router {Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en al checar paquetes en interfaz")  
                        ifAdminstatus[Objetivos[obj].NombreDevice][interfaceEST] = estados[interfaceEST]

        if not ipInAddrErrors :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("ipInAddrErrors.0")
                if erroresmte:
                    ipInAddrErrors.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    ipInAddrErrors.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("ipInAddrErrors.0")
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if ipInAddrErrors[indice] < errorAct and errorAct > 15:
                        Alertas.EnviarAlerta(f"Se estan presentando errores de packetes en su destion posible intento de ataque en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en destino, posible ataque")  
                        ipInAddrErrors[indice] = errorAct
                        indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        if not icmpInErrors :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("icmpInErrors.0")
                if erroresmte:
                    icmpInErrors.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    icmpInErrors.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("icmpInErrors.0")
                catidad = icmpInErrors[indice] +15
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if icmpInErrors[indice] < errorAct and errorAct > catidad:
                        Alertas.EnviarAlerta(f"Se estan presentando errores de packetes ICMP en interfaz en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en destino, posible ataque")  
                        icmpInErrors[indice] = errorAct
                        indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        if not tcpInErrs :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("tcpInErrs.0")
                if erroresmte:
                    tcpInErrs.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    tcpInErrs.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("tcpInErrs.0")
                catidad = tcpInErrs[indice] +15
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if tcpInErrs[indice] < errorAct and errorAct > catidad:
                        Alertas.EnviarAlerta(f"Se estan presentando errores de packetes TCP en interfaz en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en destino, posible ataque")  
                        tcpInErrs[indice] = errorAct
                        indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        if not udpInErrs :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("udpInErrors.0")
                if erroresmte:
                    udpInErrs.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    udpInErrs.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP("udpInErrors.0")
                catidad = udpInErrs[indice] +15
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if udpInErrs[indice] < errorAct and errorAct > catidad:
                        Alertas.EnviarAlerta(f"Se estan presentando errores de packetes UDP en interfaz en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en destino, posible ataque")  
                        udpInErrs[indice] = errorAct
                        indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        if not cpmCPUTotal1minRev_Count :
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP(f"{cpmCPUTotal1minRev}.1")
                if erroresmte:
                    cpmCPUTotal1minRev_Count.append(int(erroresmte.strip().split(" ")[3]))
                else: 
                    cpmCPUTotal1minRev_Count.append(0)
        else:
            indice = 0
            for obj in Objetivos.keys():
                erroresmte = Objetivos[obj].getSNMP(f"{cpmCPUTotal1minRev}.1")
                if erroresmte:
                    errorAct = int(erroresmte.strip().split(" ")[3])
                    if cpmCPUTotal1minRev_Count[indice] < errorAct:
                        if errorAct > 80:
                            Alertas.EnviarAlerta(f"Se estan presentando errores de packetes UDP en interfaz en el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Errores en destino, posible ataque")  
                    cpmCPUTotal1minRev_Count[indice] = errorAct
                    indice +=1
                else: 
                    indice += 1
                    Alertas.EnviarAlerta(f"Se callo la comunicacion con el router{Objetivos[obj].NombreDevice}, con ip:{Objetivos[obj].DestHost}",Email,"Caida de comunicacion")  

        print(f"ifAdminstatus : \n{ifAdminstatus}") 
        # Las ip directamente conectadas
        print(f"ipAdEntAddr : \n{ipAdEntAddr}") 
        #Numero de eventos fallidos
        print(f"mteEventFailures : \n{mteEventFailures}")
        # Si los saltos de ruteo estan active
        print(f"ipCidrRouteStatus : \n{ipCidrRouteStatus}")
        # packetes que antenido error dentro de ellos
        print(f"ifInErrors : \n{ifInErrors}")
        #Numero de datagramas descartados por error ip destino     
        print(f"ipInAddrErrors : \n{ipInAddrErrors}")
        #Errores de entrada ICMP     
        print(f"icmpInErrors : \n{icmpInErrors}")
        #Errores de entrada TCP checksum
        print(f"tcpInErrs : \n{tcpInErrs}")
        #Errores de entrada UDP 
        print(f"udpInErrs : \n{udpInErrs}")
        #Pocentaje de uso del CPU
        print(f"cpmCPUTotal1minRev : \n{cpmCPUTotal1minRev_Count}")
        time.sleep(60)

def Demonio_S(**Objetivos):

    for obj in Objetivos.keys():
        print(f"{obj}:{Objetivos[obj].DestHost}") 


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

    NUM_T = 1
    Hilos = []
    Hilos.append(threading.Thread(      target=Demonio_S,
                                        kwargs={
                                                SNMPServidores[0].NombreDevice:SNMPServidores[0],
                                                SNMPServidores[1].NombreDevice:SNMPServidores[1]
                                                }
                                 ))
    for num_T in range(NUM_T):
        Hilos.append(threading.Thread(  target=Demonio_R,
                                        kwargs={
                                                SNMPRouters[num_T*2].NombreDevice:SNMPRouters[num_T*2],
                                                SNMPRouters[(num_T*2)+1].NombreDevice:SNMPRouters[(num_T*2)+1]
                                                }
                                    ))
    for h in Hilos:    
        h.start()
        
if __name__ == "__main__":
    main()