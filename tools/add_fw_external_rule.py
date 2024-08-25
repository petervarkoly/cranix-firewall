#!/usr/bin/python3
# Copyright 2024 Dipl. Ing. Peter Varkoly <pvarkoly@cephalix.eu>. All rights reserved.
import json
import os
import sys

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"

config = json.load(open(CRANIX_FW_CONFIG))
if sys.argv[1] not in config["nat_rules"]["external"]:
    config["nat_rules"]["external"] = { sys.argv[1]: "" }
    with open(CRANIX_FW_CONFIG,"w") as f:
        json.dump(config, f, indent=True)
    os.system("/usr/sbin/crx_firewall.py")
