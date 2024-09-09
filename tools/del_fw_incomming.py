#!/usr/bin/python3
# Copyright 2024 Dipl. Ing. Peter Varkoly <pvarkoly@cephalix.eu>. All rights reserved.
import json
import os
CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"

rule=input("")
config = json.load(open(CRANIX_FW_CONFIG))
if rule in config["open_ports"]["external"]:
    config["open_ports"]["external"].remove(rule)
    with open(CRANIX_FW_CONFIG,"w") as f:
        json.dump(config, f, indent=True)
    os.system("/usr/sbin/crx_firewall.py")
