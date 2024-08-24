#!/bin/bash

if [ -e /etc/cranix-firewall.conf ]; then
	exit
fi
./etc/sysconfig/cranix
INT_DEV=$( ip addr | gawk "/$CRANIX_SERVER/ { print \$NF }" )
EXT_DEV=$( ip route | gawk '{if( $1 == "default" ) { print $5 }}' )
sed s/#INT_DEV#/$INT_DEV/ /usr/share/cranix/templates/firewall/cranix-firewall-template.conf > /etc/cranix-firewall.conf
sed -i s/#EXT_DEV#/$EXT_DEV/  /etc/cranix-firewall.conf
sed -i s/#CRANIX_SERVER_NET#/$CRANIX_SERVER_NET/ /etc/cranix-firewall.conf
sed -i s/#CRANIX_SERVER_EXT_IP#/$CRANIX_SERVER_EXT_IP/ /etc/cranix-firewall.conf
if [ -e /etc/firewalld/zones/external.xml ]; then
	/usr/share/cranix/tools/firewall/convert_firewalld_to_cranix.py
fi
