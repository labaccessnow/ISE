# Identity Services Engine (ISE) & Zero-Trust NAC

Designing and operating Cisco Identity Services Engine as the policy core of a
Zero-Trust network — every user and device is continuously identified, profiled,
and authorized before it touches the network, wired or wireless.

## What I work on
- **Policy architecture** — authentication and authorization policy sets, downloadable
  ACLs and dynamic VLAN assignment, device profiling and posture.
- **802.1X / EAP-TLS** — certificate-based onboarding for managed endpoints against
  Active Directory and an internal CA, with MAB fallback for headless devices.
- **TACACS+ device administration** — role-based command authorization for the
  network estate (ISE is the one NAC platform that also does TACACS+).
- **Wireless + wired NADs** — Catalyst 9800 WLCs and Catalyst switches as RADIUS
  clients, including CoA / change-of-authorization.
- **Lifecycle** — certificate management, AD/LDAP integration, and HA deployment;
  ISE 3.4 (PAC-less TrustSec).

## Reference build
[`ise-demo-enclave`](https://github.com/labaccessnow/ise-demo-enclave) — a self-contained,
fully automated **Cisco ISE 3.4 + Windows Server AD** lab on Proxmox. One Ansible role
provisions both nodes, the domain controller promotes unattended (forest + DNS +
authoritative NTP), and the ISE setup wizard is driven over serial. Every gotcha documented.

Lead engineer for a production Cisco ISE / Zero-Trust deployment across enterprise and federal networks.
