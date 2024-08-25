#!/usr/bin/python3
# Offene Ports für spezifische IP-Bereiche
import json
import subprocess

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))

for pre in config.get("pre_rules", []):
    subprocess.run(pre, shell=True)

# Open ports to devices
for zone, ip_ports in config.get("open_ports", {}).items():
    device = config['devices'][zone]
    for port in ip_ports:
        num, prot = port.split("/")
        command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -j ACCEPT"
        subprocess.run(command, shell=True)

# Open ports to devices from ip adressess
for zone, ip_ports in config.get("open_ports_with_ip", {}).items():
    device = config['devices'][zone]
    for ip_range, ports in ip_ports.items():
        for port in ports:
            num, prot = port.split("/")
            command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -s {ip_range} -j ACCEPT"
            subprocess.run(command, shell=True)

# NAT rules
for zone, nat_rules in config.get("nat_rules", {}).items():
    device = config['devices'][zone]
    for ip_range, to_source in nat_rules.items():
        if to_source == "":
            command = f"/usr/sbin/iptables -t nat -A POSTROUTING -s {ip_range} -o {device} -j MASQUERADE"
        else:
            command = f"/usr/sbin/iptables -t nat -A POSTROUTING -s {ip_range} -o {device} -j SNAT --to-source {to_source}"
        subprocess.run(command, shell=True)
        command = f"/usr/sbin/iptables -A FORWARD -s {ip_range} -o {device} -j ACCEPT"
        subprocess.run(command, shell=True)

# Port forwarding rules.
for zone, port_forward_rules in config.get("port_forward_rules", {}).items():
    device = config['devices'][zone]
    for rule in port_forward_rules:
        command = f"/usr/sbin/iptables -t nat -A PREROUTING -p {rule['proto']} -i {rule['device']} -dport {rule['dport']} -j DNAT --to-destination {rule['to_ip']}:{rule['to_port']}"
        subprocess.run(command, shell=True)
        command = f"/usr/sbin/iptables -A FORWARD -p {rule['proto']} -d {rule['to_ip']} --dport 8080 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT"
        subprocess.run(command, shell=True)

for post in config.get("post_rules", []):
    subprocess.run(post, shell=True)

