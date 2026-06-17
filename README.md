# Identity Services Engine (ISE) & Zero-Trust NAC

Design and operation of Cisco Identity Services Engine for 802.1X / MAB network
access control and Zero-Trust segmentation across wired and wireless.

## Focus
- Authentication / authorization policy sets, profiling, posture, and TACACS+ device admin
- 802.1X (EAP-TLS) and MAB onboarding against Active Directory and an internal CA
- Integration with Catalyst 9800 wireless and Catalyst switching as RADIUS NADs
- Certificate lifecycle and high-availability deployment

## Reference build
[`ise-demo-enclave`](https://github.com/labaccessnow/ise-demo-enclave) — a self-contained,
fully automated Cisco ISE 3.4 + Windows Server AD lab on Proxmox: one Ansible role provisions
both nodes, the DC promotes unattended, and ISE setup is driven over serial. Every gotcha is documented.

Part of ongoing Zero-Trust work for enterprise and federal networks.
