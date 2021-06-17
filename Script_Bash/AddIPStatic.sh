#!/usr/bin/env bash

echo "Agregando IP statica"

echo -n "Ingrese la interfaz de red: "
read interface

echo -n "Ingrese la ip para la interfaz de red ${interface}: "
read ip

echo -n "Ingrese la mascara de red en formato extendido: "
read netmask


echo -n "Ingrese la ip de gateway de la red: "
read gateway

echo -n "Ingrese la ip de red: "
read netIP

echo -n "Ingrese la ip de broadcast de la red: "
read broadcastIP

echo -e "auto ${interface}\niface ${interface} inet static\n\taddress ${ip}\n\tnetmask ${netmask}\n\tgateway ${gateway}\n\tnetwork ${netIP}\n\tbroadcast ${broadcastIP}\n\tup echo nameserver 8.8.8.8 > /etc/resolv.conf" > /etc/network/interfaces


