#!/bin/bash

./etc/sysconfig/cranix
INT_DEV=$( ip addr | gawk "/$CRANIX_SERVER/ { print \$NF }" )
EXT_DEV=$( ip addr | gawk "/$CRANIX_EXT_IP/ { print \$NF }" )
sed s/#INT_DEV#/$INT_DEV/ /usr/share/doc/packages/cranix-firewall/cranix-firewall-template.conf > /etc/cranix-firewall.conf
sed -i s/#EXT_DEV#/$EXT_DEV/  /etc/cranix-firewall.conf
sed -i s/#CRANIX_SERVER_NET#/$CRANIX_SERVER_NET/ /etc/cranix-firewall.conf
sed -i s/#CRANIX_SERVER_EXT_IP#/$CRANIX_SERVER_EXT_IP/ /etc/cranix-firewall.conf

