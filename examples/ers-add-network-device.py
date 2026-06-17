#!/usr/bin/env python3
"""Register a network device (NAD) in ISE via the ERS API.

Adding switches/WLCs by hand in the GUI doesn't scale and isn't reviewable. This is the
same object — a RADIUS client with a shared secret — created idempotently from code.

    export ISE_HOST=ise1.demo.lab
    export ISE_ERS_USER=ers-admin ISE_ERS_PASS=...   # ERS admin, not the GUI admin
    export NAD_SECRET=...                             # the RADIUS shared secret
    python3 ers-add-network-device.py sw-access-01 0.0.0.0

Enable the ERS API first: Administration > Settings > API Settings > ERS (Read/Write).
"""
import os
import sys
import requests

requests.packages.urllib3.disable_warnings()  # ISE ships a self-signed cert in the lab


def add_nad(name: str, ip: str) -> None:
    host = os.environ["ISE_HOST"]
    auth = (os.environ["ISE_ERS_USER"], os.environ["ISE_ERS_PASS"])
    body = {
        "NetworkDevice": {
            "name": name,
            "NetworkDeviceIPList": [{"ipaddress": ip, "mask": 32}],
            "authenticationSettings": {
                "radiusSharedSecret": os.environ["NAD_SECRET"],
            },
            # group it so policy can match on Device Type / Location later
            "NetworkDeviceGroupList": [
                "Device Type#All Device Types#Switch",
                "Location#All Locations",
            ],
        }
    }
    r = requests.post(
        f"https://{host}:9060/ers/config/networkdevice",
        json=body,
        auth=auth,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        verify=False,   # point at the ISE CA bundle in production
        timeout=30,
    )
    if r.status_code == 201:
        print(f"created NAD {name} ({ip}) -> {r.headers.get('Location')}")
    elif r.status_code == 400 and "already exists" in r.text:
        print(f"NAD {name} already exists — nothing to do")  # idempotent re-runs
    else:
        sys.exit(f"ERS error {r.status_code}: {r.text}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: ers-add-network-device.py <name> <ip>")
    add_nad(sys.argv[1], sys.argv[2])
