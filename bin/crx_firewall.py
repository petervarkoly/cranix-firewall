#!/usr/bin/python3
# Offene Ports für spezifische IP-Bereiche
import json
import subprocess

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))

for pre in config.get("pre_rules", []):
    subprocess.run(pre, shell=True)

for zone, ip_ports in config.get("open_ports", {}).items():
    device = config['devices'][zone]
    for port in ip_ports:
        num, prot = port.split("/")
        command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -j ACCEPT"
        subprocess.run(command, shell=True)

for zone, ip_ports in config.get("open_ports_with_ip", {}).items():
    device = config['devices'][zone]
    for ip_range, ports in ip_ports.items():
        for port in ports:
            num, prot = port.split("/")
            command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -s {ip_range} -j ACCEPT"
            subprocess.run(command, shell=True)

# NAT-Regeln
for zone, nat_rules in config.get("nat_rules", {}).items():
    device = config['devices'][zone]
    for ip_range, target_ip in nat_rules.items():
        if target_ip == "":
            command = f"/usr/sbin/iptables -t nat -A POSTROUTING -s {ip_range} -o {device} -j MASQUERADE"
        else:
            command = f"/usr/sbin/iptables -t nat -A POSTROUTING -s {ip_range} -o {device} -j SNAT --to-source {target_ip}"
        subprocess.run(command, shell=True)
        command = f"/usr/sbin/iptables -A FORWARD -s {ip_range} -o {device} -j ACCEPT"
        subprocess.run(command, shell=True)

for zone, port_forward_rules in config.get("port_forward_rules", {}).items():
    device = config['devices'][zone]
    for proto, dport, target_ip, target_port in port_forward_rules.items():
        command = f"/usr/sbin/iptables -t nat -A PREROUTING -p {proto} -i {device} -dport {dport} -j DNAT --to-destination {target_ip}:{target_port}"
        subprocess.run(command, shell=True)
        command = f"/usr/sbin/iptables -A FORWARD -p {proto} -d {target_ip} --dport 8080 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT"
        subprocess.run(command, shell=True)

for post in config.get("post_rules", []):
    subprocess.run(post, shell=True)

