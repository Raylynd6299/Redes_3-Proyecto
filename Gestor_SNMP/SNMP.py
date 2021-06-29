#!/usr/bin/env python3
import os

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


def InfoIntRouter(SNMPRouter = None):

    if SNMPRouter == None:
        return None

    int_IP_Num = {}
    IP_MASK = {}

    limpiar = lambda info: [ linea.strip().split(" ")[3]  for linea in (info.strip().split("\n")) ]

    info_ifDescr        = SNMPRouter.walkSNMP("ifDescr")
    info_ifAdminStatus  = SNMPRouter.walkSNMP("ifAdminStatus")
    info_ipAdEntNetMask = SNMPRouter.walkSNMP("ipAdEntNetMask")
    info_ifName         = SNMPRouter.walkSNMP("ifName")
    info_ipAdEntIfIndex = SNMPRouter.walkSNMP("ipAdEntIfIndex")

    if not( info_ifDescr and info_ifAdminStatus and info_ipAdEntNetMask and info_ifName and info_ipAdEntIfIndex ):
        print(f"Error Obteniendo informacion del Router {SNMPRouter.NombreDevice}")
        return False

    info_ipAdEntIfIndex = info_ipAdEntIfIndex.strip().split("\n")
    info_ipAdEntNetMask = info_ipAdEntNetMask.strip().split("\n")
    
    interfaces  = limpiar(info_ifDescr)        
    estado      = limpiar(info_ifAdminStatus)  
    contraccion = limpiar(info_ifName)

    for mask in info_ipAdEntNetMask:
        mascara = mask.split(" ")[3]
        ip = mask.split(" ")[0].split(".")[1:]
        ip = ".".join(ip)
        IP_MASK[ip] = mascara
    
    for linea in info_ipAdEntIfIndex:
        indice = int(linea.split(" ")[3])
        ip = linea.split(" ")[0].split(".")[1:]
        ip = ".".join(ip)
        int_IP_Num[indice] = list()
        int_IP_Num[indice].append(ip)
        if IP_MASK.get(ip) :
            int_IP_Num[indice].append( IP_MASK[ip] )
    
    INFO_ROUTER_SNMP = list()
    if interfaces:
        for numInt in range(len(interfaces)):
            INFO_ROUTER_SNMP.append(list()) 
            INFO_ROUTER_SNMP[numInt].append( interfaces[numInt]     )
            INFO_ROUTER_SNMP[numInt].append( contraccion[numInt]    )
            INFO_ROUTER_SNMP[numInt].append( estado[numInt]         )
            if int_IP_Num.get(numInt+1):
                INFO_ROUTER_SNMP[numInt].extend( int_IP_Num[numInt+1] )
    else:
        print("Error al obtener informacion de las interfaces")
        return False
    
    print(f"Router: {SNMPRouter.NombreDevice}")
    for interface in INFO_ROUTER_SNMP:
        cadena = f"          {interface[0]:16}   {interface[1]:6}   {interface[2]:7}"
        if len(interface) == 5:
            cadena += f"   {interface[3]:15} {interface[4]:16}"
        print(cadena)

    return True


def InfoActividadRouter(SNMPRouter = None):

    if SNMPRouter == None:
        return None

    int_IP_Num = {}
    IP_MASK = {}

    limpiar = lambda info: [ linea.strip().split(" ")[3]  for linea in (info.strip().split("\n")) ]

    info_ifDescr        = SNMPRouter.walkSNMP("ifDescr")
    info_ifAdminStatus  = SNMPRouter.walkSNMP("ifAdminStatus")
    info_ipAdEntNetMask = SNMPRouter.walkSNMP("ipAdEntNetMask")
    info_ipAdEntIfIndex = SNMPRouter.walkSNMP("ipAdEntIfIndex")

    if not( info_ifDescr and info_ifAdminStatus and info_ipAdEntNetMask and info_ipAdEntIfIndex ):
        print(f"Error Obteniendo informacion del Router {SNMPRouter.NombreDevice}")
        return False

    info_ipAdEntIfIndex = info_ipAdEntIfIndex.strip().split("\n")
    info_ipAdEntNetMask = info_ipAdEntNetMask.strip().split("\n")
    
    interfaces  = limpiar(info_ifDescr)        
    estado      = limpiar(info_ifAdminStatus)  

    for mask in info_ipAdEntNetMask:
        mascara = mask.split(" ")[3]
        ip = mask.split(" ")[0].split(".")[1:]
        ip = ".".join(ip)
        IP_MASK[ip] = mascara
    
    for linea in info_ipAdEntIfIndex:
        indice = int(linea.split(" ")[3])
        ip = linea.split(" ")[0].split(".")[1:]
        ip = ".".join(ip)
        int_IP_Num[indice] = list()
        int_IP_Num[indice].append(ip)
        if IP_MASK.get(ip) :
            int_IP_Num[indice].append( IP_MASK[ip] )
    
    INFO_ROUTER_SNMP = list()
    if interfaces:
        for numInt in range(len(interfaces)):
            INFO_ROUTER_SNMP.append(list()) 
            INFO_ROUTER_SNMP[numInt].append( interfaces[numInt]     )
            INFO_ROUTER_SNMP[numInt].append( estado[numInt]         )
            if int_IP_Num.get(numInt+1):
                INFO_ROUTER_SNMP[numInt].extend( int_IP_Num[numInt+1] )
    else:
        print("Error al obtener informacion de las interfaces")
        return False

    print(f"Router: {SNMPRouter.NombreDevice}")
    for interface in INFO_ROUTER_SNMP:
        if "up" in interface[1]:    
            if len(interface) == 4:
                cadena = f"          {interface[0]:16}   {interface[1]:7}   {interface[2]:15} {interface[3]:16}"
            if len(interface) == 2:
                cadena = f"          {interface[0]:16}   {interface[1]:7}"
            print(cadena)

    return True