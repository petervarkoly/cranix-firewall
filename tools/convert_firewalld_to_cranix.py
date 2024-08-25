#!/usr/bin/python3
from lxml import etree
import json

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))

with open("/etc/firewalld/zones/external.xml") as f:
    tree = etree.parse(f)
    ports = tree.xpath('/zone/port')
    if type(ports) is list:
        for tag in ports:
            port = tag.get("port") + "/" +tag.get("protocol")
            if port not in config["open_ports"]["external"]:
                config["open_ports"]["external"].append(port)
    ports = tree.xpath('/zone/forward-port')
    if type(ports) is list:
        for tag in ports:
            rule = {
                "proto": tag.get("protocol"),
                "dport": tag.get("port"),
                "to_addr": tag.get("to-addr"),
                "to_port": tag.get("to-port"),
            }
            if rule not in config["port_forward_rules"]["external"]:
                config["port_forward_rules"]["external"].append(rule)
    rules = tree.xpath('/zone/rule')
    if type(rules) is list:
        for tag in rules:
            if tag[1].tag == "masquerade":
                config["nat_rules"]["external"][tag[0].get("address")] = ""
with open(CRANIX_FW_CONFIG,"w") as f:
    json.dump(config, f, indent=True)
