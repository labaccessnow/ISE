# Downloadable ACL + a safe rollout to closed mode

A dACL is how ISE enforces *what* an authenticated endpoint can reach — the authorization
result, not just "let them on." ISE stores the ACL centrally and pushes it to the switchport
at authorization time, so you change access policy in one place instead of touching every NAD.

## The dACL (defined in ISE, pushed to the port)

This is the ACL content you paste into **Policy > Policy Elements > Results > Authorization >
Downloadable ACLs**. Example: a contractor profile — DHCP/DNS and internal web only, nothing else.

```
permit udp any eq bootpc any eq bootps      ! DHCP
permit udp any any eq domain                 ! DNS
permit tcp any 0.0.0.0 0.0.255.255 eq 443   ! internal HTTPS only
deny   ip any any
```

You reference that dACL from an **Authorization Profile**, and a policy rule
(e.g. `IdentityGroup == Contractors`) returns that profile. The switch downloads and
applies it per session.

## Roll it out without locking anyone out

The mistake is going straight to enforcement. Do it in stages:

1. **Monitor mode (open).** Leave the port `access-session` open — authenticate, log, but
   don't drop anything. Watch ISE **Live Logs** for who *would* have failed.
2. **Low-impact mode.** Apply a permissive pre-auth ACL so unauthenticated devices still
   get DHCP/DNS/PXE, then layer the dACL on success.
3. **Closed mode.** Only once Live Logs are clean, flip the port to `access-session closed`.

```
! verify what actually landed on the session:
show access-session interface gi1/0/10 details
show ip access-lists interface gi1/0/10        ! the dACL ISE pushed, live on the port
```

## Lesson learned
The dACL that "didn't work" almost always *did* — the session just never reached the
authorization step. Check `show access-session` first: if it's not `Authz Success`, the
problem is upstream (RADIUS reachability, policy match), not the ACL.
