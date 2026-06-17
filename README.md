# Identity Services Engine (ISE) & Zero-Trust NAC

ISE is the policy decision point in a Zero-Trust network: discover, profile, authenticate,
and authorize every endpoint — and revoke access the instant a session goes bad. I've run it
as the access-control core for enterprise and federal networks, wired and wireless.

## What it looks like in practice

The switch (the NAD) does the enforcement; ISE makes the decision. Here's the IOS-XE side
done the modern way — **IBNS 2.0**, with concurrent 802.1X + MAB and CoA wired in so ISE can
quarantine a live session:

```text
! --- RADIUS to ISE, with change-of-authorization for quarantine ---
radius server ISE-1
 address ipv4 0.0.0.0 auth-port 1812 acct-port 1813
 key <shared-secret>
aaa group server radius ISE
 server name ISE-1
 ip radius source-interface Vlan10
aaa server radius dynamic-author          ! CoA: ISE can bounce/quarantine a session
 client 0.0.0.0 server-key <shared-secret>
aaa authentication dot1x default group ISE
aaa authorization network default group ISE
aaa accounting dot1x default start-stop group ISE

! --- IBNS 2.0 control policy: try 802.1X and MAB at the same time ---
policy-map type control subscriber DOT1X_MAB
 event session-started match-all
  10 class always do-all
   10 authenticate using dot1x priority 10
   20 authenticate using mab priority 20

interface GigabitEthernet1/0/10
 switchport access vlan 10
 switchport mode access
 access-session host-mode multi-auth
 access-session port-control auto
 ! access-session closed        <-- leave this OFF until monitor mode proves the policy
 dot1x pae authenticator
 service-policy type control subscriber DOT1X_MAB
```

## Best practices I follow
- **Phase it: Monitor → Low-Impact → Closed.** Authentication runs and logs, but the port
  stays open, until the policy is proven. Only then flip `access-session closed`.
- **Certificates, not passwords.** EAP-TLS with machine + user certs from an internal CA;
  MAB only for gear that genuinely can't do 802.1X.
- **Distributed personas.** Separate PAN / MnT / PSN, two of each for HA; size PSNs to the
  endpoint count, not the org chart.
- **Revocation is the whole point.** If you can't CoA a bad session off the network in
  seconds, it isn't Zero Trust — it's a login page.

## Lessons learned
- **`aaa new-model` will lock you out of the box.** Enable it on a fresh switch/WLC without
  also setting `aaa authentication enable default enable`, and `enable` over SSH returns
  *"% Error in authentication"* — you're stuck in user EXEC. Put the login/enable/exec methods
  in the *same* change, or fix it from the console. (Cost me a recovery trip the first time.)
- **ISE silently drops RADIUS from a NAD it doesn't know.** No reject, no obvious log —
  `test aaa` just times out while you blame the shared secret. Add the network device in ISE
  *first*, then test.
- **Closed mode on day one black-holes a floor of users.** I learned to live in Monitor Mode
  for weeks and read the live logs before tightening anything.
- **Expired system/EAP certs take auth down quietly.** Monitor expiry; automate renewal.

## Where the platform is
- **3.3 (Jul 10, 2023):** TLS 1.3 for EAP-TLS.
- **3.4 (Aug 5, 2024):** native Duo identity sync, AD domain-controller failover, pxGrid Direct.
- **3.5 (Sep 18, 2025):** SNMPv3 profiling for non-authenticating IoT, cloud Multi-Factor Classification.

## Reference build
**[ise-demo-enclave](https://github.com/labaccessnow/ise-demo-enclave)** — a fully automated
ISE 3.4 + Windows AD lab on Proxmox (one Ansible role builds both nodes; serial-driven ISE setup).
