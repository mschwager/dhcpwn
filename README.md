# DHCPwn

DHCPwn is a tool used for testing `DHCP` `IP` exhaustion attacks. It can also be
used to sniff local `DHCP` traffic.

Useful links:

* https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol
* https://tools.ietf.org/html/rfc2131
* https://en.wikipedia.org/wiki/Bootstrap_Protocol
* https://tools.ietf.org/html/rfc951

# Overview

The `DHCP` protocol is connectionless and implemented via `UDP`. These two
characteristics allow this attack to be performed. Since there is no actual
connection being made between the client and server we can quickly send many
spoofed requests.

`DHCP` servers rely on the senders `MAC` address to allocate `IP` addresses. We can
easily spoof many requests with different, fake `MAC` addresses. This will
eventually exhaust the server's ability to assign new `IP` addresses. Depending
on the server's method of releasing `IP` addresses associated with a given `MAC`
address this attack will either be more, or less effective. For example, if
a server quickly releases allocations that it doesn't receive responses from,
the attack will be less effective.

This attack is typically considered to be a form of DoS.

# Installing

```
$ pip install https://github.com/mschwager/dhcpwn
```

OR

```
$ git clone https://github.com/mschwager/dhcpwn.git
$ pip install -r requirements.txt
```

# Using

Flood:

```
$ dhcpwn --interface wlan0 flood --count 256
```

Sniff:

```
$ dhcpwn --interface wlan0 sniff
```

Help:

```
$ dhcpwn -h
```
