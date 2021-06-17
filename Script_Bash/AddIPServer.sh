#!/usr/bin/env bash
echo -n "Ingresa la interfaz de red: "
read interface
echo -n "Ingresa la ip que deseas utilizar para la interfaz: "
read ip
echo -n "Ingresa la contraccion de la mascara que utilizas para la interfaz ${interface}: "
read prefix
echo -n "Ingresa la ip del gateway: "
read gate
ip route flush dev ${interface}
ip addr add ${ip}/${prefix} dev ${interface}
ip route add default via ${gate}
echo "Listo !!"
