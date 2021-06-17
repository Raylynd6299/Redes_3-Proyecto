#!/usr/bin/env python3
import os

INFO_ROUTERS_SNMP = None

HOSTNAME_OID = "1.3.6.1.2.1.1.5.0"
DESCR_OID = "1.3.6.1.2.1.1.1.0"
CONTACT_OID = "1.3.6.1.2.1.1.4.0"
LOCATION_OID = "1.3.6.1.2.1.1.6.0"
INTERFACE_OID = "1.3.6.1.2.1.2.2.1"
INTNUMBER_OID = "1.3.6.1.2.1.2.1.0"

class Snmp(object):
    """
    SNMP
    """
    def __init__(self, nombreDevice="", version=3, userName="Ray", destHost="localhost",secLevel="authPriv", protAuth="MD5", protEnc="DES", passAuth="Password", encPhrase="" ):
        self.NombreDevice = nombreDevice
        self.Version = version
        self.UserName = userName
        self.DestHost = destHost
        self.SecLevel = secLevel
        self.ProtAuth = protAuth
        self.ProtEnc = protEnc
        self.PassAuth = passAuth
        if(encPhrase == ""):
            self.EncPhrase = passAuth
        else:
            self.EncPhrase = encPhrase
 
    def getSNMP(self, OID=DESCR_OID):
        """
        Obtener información de snmp
        """
        try:
            result = os.popen(f'snmpget -u {self.UserName} -l {self.SecLevel} -a {self.ProtAuth} -x {self.ProtEnc} -A {self.PassAuth} -X {self.EncPhrase} {self.DestHost} {OID}').read()
        except Exception as e:
            result = None
        return result
    def walkSNMP(self, OID=""):
        """
        Obtener información de snmp
        """
        try:
            result = os.popen(f'snmpwalk -u {self.UserName} -l {self.SecLevel} -a {self.ProtAuth} -x {self.ProtEnc} -A {self.PassAuth} -X {self.EncPhrase} {self.DestHost} {OID}').read()
        except Exception as e:
            result = None
        return result

def main():
    
    global INFO_ROUTERS_SNMP

    Servidor_1 = Snmp(nombreDevice="Servidor 1", userName="R3SNMP",destHost="192.168.226.18",protAuth="SHA-256",passAuth="RaDa22962")
    Servidor_2 = Snmp(nombreDevice="Servidor 2", userName="R3SNMP",destHost="192.168.226.26",protAuth="SHA-256",passAuth="RaDa22962")
    Router_1 = Snmp(nombreDevice="Router 1", userName="R3SNMP",destHost="192.168.226.49",protAuth="SHA",passAuth="RaDa22962")
    Router_2 = Snmp(nombreDevice="Router 2", userName="R3SNMP",destHost="192.168.226.50",protAuth="SHA",passAuth="RaDa22962")
    Router_3 = Snmp(nombreDevice="Router 3", userName="R3SNMP",destHost="192.168.226.54",protAuth="SHA",passAuth="RaDa22962")
    Router_4 = Snmp(nombreDevice="Router 4", userName="R3SNMP",destHost="192.168.226.58",protAuth="SHA",passAuth="RaDa22962")
    Router_5 = Snmp(nombreDevice="Router 5", userName="R3SNMP",destHost="192.168.226.33",protAuth="SHA",passAuth="RaDa22962")
    Router_6 = Snmp(nombreDevice="Router 6", userName="R3SNMP",destHost="192.168.226.42",protAuth="SHA",passAuth="RaDa22962")

    
    infoR1_ifDescr = Router_4.walkSNMP("ifDescr")
    infoR1_ifAdminStatus = Router_4.walkSNMP("ifAdminStatus")
    infoR1_ipAdEntNetMask = Router_4.walkSNMP("ipAdEntNetMask")
    infoR1_ifName = Router_4.walkSNMP("ifName")
    infoR1_ipAdEntIfIndex = Router_4.walkSNMP("ipAdEntIfIndex")

    limpiar = lambda info: [ linea.strip().split(" ")[3]  for linea in (info.strip().split("\n")) ]

    infoR1_ipAdEntIfIndex = infoR1_ipAdEntIfIndex.strip().split("\n")
    infoR1_ipAdEntNetMask = infoR1_ipAdEntNetMask.strip().split("\n")
    
    int_IP_Num = {}
    IP_MASK = {}

    for mask in infoR1_ipAdEntNetMask:
        mascara = mask.split(" ")[3]
        ip = mask.split(" ")[0].split(".")
        ip = ".".join(ip[1:])
        
        IP_MASK[ip] = mascara

    for linea in infoR1_ipAdEntIfIndex:
        indice = int(linea.split(" ")[3])
        ip = linea.split(" ")[0].split(".")
        ip = ".".join(ip[1:])

        int_IP_Num[indice] = list()
        int_IP_Num[indice].append(ip)

        if IP_MASK.get(ip) :
            int_IP_Num[indice].append( IP_MASK[ip] )


    interfaces = limpiar(infoR1_ifDescr)        
    estado = limpiar(infoR1_ifAdminStatus)  
    contraccion = limpiar(infoR1_ifName)

    INFO_ROUTERS_SNMP = dict()

    if interfaces:
        INFO_ROUTERS_SNMP[Router_4.NombreDevice] = list()
        for numInt in len(interfaces):
            INFO_ROUTERS_SNMP[Router_4.NombreDevice].append(list()) 
            INFO_ROUTERS_SNMP[Router_4.NombreDevice][numInt].append( interfaces[numInt]     )
            INFO_ROUTERS_SNMP[Router_4.NombreDevice][numInt].append( contraccion[numInt]    )
            INFO_ROUTERS_SNMP[Router_4.NombreDevice][numInt].append( estado[numInt]         )
            if int_IP_Num.get(numInt+1):
                INFO_ROUTERS_SNMP[Router_4.NombreDevice][numInt].extend( int_IP_Num[numInt] )
    else:
        print("Error al obtener informacion de las interfaces")

    print(int_IP_Num)
    print(INFO_ROUTERS_SNMP)
    #print(f"La informacion ifDescr del { Router_1.NombreDevice } es:\n {infoR1_ifDescr}")
    #print(f"La informacion ifAdminStatus del { Router_1.NombreDevice } es:\n {infoR1_ifAdminStatus}")
    #print(f"La informacion ipAdEntNetMask del { Router_1.NombreDevice } es:\n {infoR1_ipAdEntNetMask}")
    #print(f"La informacion ifName del { Router_1.NombreDevice } es:\n {infoR1_ifName}")
    #print(f"La informacion ipAdEntIfIndex del { Router_1.NombreDevice } es:\n {infoR1_ipAdEntIfIndex}")

    #print(f"La informacion del {Servidor_1.NombreDevice} es:\n {infoS1}")
    #print(f"La informacion del {Servidor_2.NombreDevice} es:\n {infoS2}")
    #print(f"La informacion del { Router_1.NombreDevice } es:\n {infoR1}")
    #print(f"La informacion del { Router_2.NombreDevice } es:\n {infoR2}")
    #print(f"La informacion del { Router_3.NombreDevice } es:\n {infoR3}")
    #print(f"La informacion del { Router_4.NombreDevice } es:\n {infoR4}")
    #print(f"La informacion del { Router_5.NombreDevice } es:\n {infoR5}")
    #print(f"La informacion del { Router_6.NombreDevice } es:\n {infoR6}")
                                                                                                                                                                                                                                            



if __name__ == "__main__":
    main()