#!/usr/bin/python3
# Offene Ports für spezifische IP-Bereiche
import json
import subprocess

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))

for basic in config.get("basic_rules", []):
    subprocess.run(basic, shell=True)

for interface, ip_ports in config.get("open_ports", {}).items():
    for port in ip_ports:
        num, prot = port.split("/")
        command = f"iptables -A INPUT -i {interface} -p {prot} --dport {num} -j ACCEPT"
        subprocess.run(command, shell=True)

for interface, ip_ports in config.get("open_ports_with_ip", {}).items():
    for ip_range, ports in ip_ports.items():
        for port in ports:
            num, prot = port.split("/")
            command = f"iptables -A INPUT -i {interface} -p {prot} --dport {num} -s {ip_range} -j ACCEPT"
            subprocess.run(command, shell=True)

# NAT-Regeln
for interface, nat_rules in config.get("nat_rules", {}).items():
    for ip_range, target_ip in nat_rules.items():
        if target_ip == "":
            command = f"iptables -t nat -A POSTROUTING -s {ip_range} -o {interface} -j MASQUERADE"
        else:
            command = f"iptables -t nat -A POSTROUTING -s {ip_range} -o {interface} -j SNAT --to-source {target_ip}"
        subprocess.run(command, shell=True)
        command = f"/usr/sbin/iptables -A FORWARD -s {ip_range} -o {interface} -j ACCEPT"
        subprocess.run(command, shell=True)
