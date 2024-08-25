#!/usr/bin/python3
# Copyright 2024 Dipl. Ing. Peter Varkoly <pvarkoly@cephalix.eu>. All rights reserved.
import json
import os
import sys

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"

#Read new services and ports from standard input
config = json.load(open(CRANIX_FW_CONFIG))

try:
    del config["nat_rules"]["external"][sys.argv[1]]
    with open(CRANIX_FW_CONFIG,"w") as f:
        json.dump(config, f, indent=True)
    os.system("/usr/sbin/crx_firewall.py")
except:
    pass

