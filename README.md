# cranix-firewall
Firewall configurator for CRANIX/CEPHALIX

cranix-firewall is a simple firewall configurations tool which kann controll the access to the CRANIX/CEPHALIX server based on a json configurations file: /etc/cranix-firewall.conf. This configuration file has following sections:

open_rules: This is an array of commands which will be executed when the firewall will be opened.

pre_rules: This is an array of commands which will be executed when the firewall will be started.

devices: In this section the network devices of the server will be ordered to zones. Normaly two zones should exist "external" and "internal". All arbitary zones can be defined. In the different rule sections the rules will be ordered in this zones.

open_ports: In this section the ports which have to been opened in a zone can be defined.

open_ports_with_ip: In this section the ports which have to been opened in a zone can be defined as in open_ports. In this section the acces can be reduced for ip adresses or ip address areas.

nat_rules: In this section NAT rules can be defined by MASQUERAD or SNAT depending on if to_source will be given.

port_forward_rules: Port forwarding rules can be defined for the zones.

post_rules: An array of commands which will be executed after all rules were set.

The firewall will be started by executing /usr/sbin/crx_firewall.py
