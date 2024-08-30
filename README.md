# cranix-firewall
Firewall configurator for CRANIX/CEPHALIX

cranix-firewall is a simple firewall configurations tool which kann controll the access to the **CRANIX/CEPHALIX** server based on a json configurations file: `/etc/cranix-firewall.conf`. This configuration file has following sections:

**open_rules**: This is an array of commands which will be executed when the firewall will be opened.

**pre_rules**: This is an array of commands which will be executed when the firewall will be started.

**devices**: Here you can assign network cards to zones. Normaly two zones should exist "external" and "internal". This assigment will be made by first start of cranix-firewall according to the network configuration. All arbitary zones can be defined. In the different rule sections the rules will be ordered in this zones.

**open_ports**: In this section the ports which have to been opened in a zone can be defined.

**open_ports_with_ip**: In this section the ports which have to been opened in a zone can be defined as in open_ports. In this section the acces can be reduced for ip adresses or ip address areas.

**nat_rules**: In this section NAT rules can be defined by MASQUERAD or SNAT depending on if to_source will be given.

**port_forward_rules**: Port forwarding rules can be defined for the zones.

**post_rules**: An array of commands which will be executed after all rules were set.

The firewall will be started by executing `/usr/sbin/crx_firewall.py`. This program accept three command line parameters:

**start** Starting the firewall. All rules will be set.

**stop** Stops the firewall. Only the base configuration will be set. The commands in section **open_rules** will be executed. The standard setting is: only outgoing and estabilished connections and connections to device **lo** will be accepted.

**open** The commands in section **open_rules** will be executed.

The standard configuration after installing cranix-firewall:

```
{
     "open_rules": [
         "iptables -t mangle -F",
         "iptables -t nat -F",
         "iptables -F",
         "iptables -P INPUT ACCEPT",
         "iptables -P FORWARD ACCEPT",
         "iptables -P OUTPUT ACCEPT"
    ],
    "pre_rules": [
        "iptables -t mangle -F",
        "iptables -t nat -F",
        "iptables -F",
        "iptables -P INPUT DROP",
        "iptables -P FORWARD DROP",
        "iptables -P OUTPUT ACCEPT",
        "iptables -I INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT",
        "iptables -I FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT",
        "iptables -I INPUT -i lo -j ACCEPT",
        "iptables -I FORWARD -o lo -j ACCEPT",
        "iptables -I FORWARD -i lo -j ACCEPT"
    ],
    "devices": {
        "external": "#EXT_DEV#",
        "internal": "#INT_DEV#"
    },
    "open_ports": {
        "external": ["ssh/tcp", "https/tcp"],
        "internal": [ ]
    },
    "open_ports_with_ip": {
        "external": { },
        "internal": { }
    },
    "nat_rules": {
        "external": [
            {
                "proto": "",
                "source": "#CRANIX_SERVER_NET#",
                "dest": "",
                "to_source": "#CRANIX_SERVER_EXT_IP#"
            }
        ],
        "internal": []
    },
    "port_forward_rules": {
        "external": [],
        "internal": []
    },
    "post_rules": [
        "/usr/share/cranix/tools/wait-for-api.sh",
        "/usr/share/cranix/tools/firewall/open_rooms.py",
        "/usr/sbin/crx_manage_room_access.py --all --set_defaults",
        "test -e /usr/share/cranix/tools/custom/fw-post-start.sh && /usr/share/cranix/tools/custom/fw-post-start.sh"
    ]
}
```

You can edit this configurtation file. After each change you have to start cranix-firewall again. This file will be modified by cranix-api if you defines new incomming outgoing or remote access rules. 
* The incomming rules take place in open_ports.external section.
* The outgoing will be writte in nat_rules.external section.
* The remote access rules you can find in port_forward_rules.external section.

The rules for room access controll are dynamically and will not be written in the firewall configuration. Please note that after all start of the firewall the actual room access control rules will be removed and the default states will be set in all dynamically controllable room.
