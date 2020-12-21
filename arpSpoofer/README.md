ARP spoofing is a Man in the Middle (MitM) type of attack in which a malicious 
actor sends falsified ARP (Address Resolution Protocol) messages over a local 
area network. ... Once the attacker's MAC address is connected to an authentic 
IP address, the attacker will begin receiving any data that is intended for 
that IP address. Also referred to as ARP poisoning, or a “contamination” of 
the ARP caches/table.

One strategy includes continually bombarding the network with false ARP replies.
While most systems ignore answer packets that can’t be assigned to a request, 
this changes as soon as a computer in the LAN starts an ARP request and so is 
willing to receive a response. Depending on timing, either the response of the 
target system or one of the fake response packets will arrive at the sender first.

tell the victim you are the router
arpspoof -i eth0 -t 10.0.2.7 10.0.2.1 

tell the router you are the victim
arpspoof -i eth0 -t 10.0.2.1 10.0.7

enable port forwarding so linux allows packets to flow through it like a router.
echo 1 > /proc/sys/net/ipv4/ip_forward
linux has this disabled as a security feature, so if we don't do this the victim
will lose its network connection. If the intercepted data packets are not forwarded, 
but are instead discarded, ARP spoofing can result in a denial of service (DoS).

Protection against data espionage can be promised by some encryption techniques 
and certificates for authentication. If an attacker only catches encoded data, 
the worst case is limited to a denial of service by discarding data packets. 
But reliable data encryption has to be implemented consistently.

Since ARP spoofing exploits the address resolution protocol, all IPv4 networks 
are prone to attacks of this kind. The implementation of IPv6 was also unable 
to solve this core problem. The new IP standard renounces ARP and instead 
controls address resolution in the LAN via NDP (Neighbor Discovery Protocol), 
which is also vulnerable to spoofing attacks. The security gap could be closed 
through the Secure Neighbor Discovery (SEND) protocol, but this isn’t supported 
by many desktop operating systems.

Possible protection from the manipulation of ARP caches is offered by static 
ARP entries, which can be set in Windows, for example, by using the command 
line program ARP and the command arp –s. But since entries of this type have 
to be made manually, these security methods are generally restricted to only 
the most important systems in the network.