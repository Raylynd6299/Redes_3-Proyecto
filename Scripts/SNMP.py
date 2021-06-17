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

def prueba():
    print("Modulos SNMP")