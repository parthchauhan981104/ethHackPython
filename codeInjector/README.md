works only for htp pages. may need to clear browser cache.

run arp spoof program first to become Man In The Middle.
If testing against remote computer run "iptables -I FORWARD -j NFQUEUE --queue-num 0" run this first to modify
FORWARD chain that is used to keep packets by default, put them in NFQUEUE, 0 identifies that queue.

For testing against local machine "iptables -I OUTPUT -j NFQUEUE --queue-num 0" this is the chain where packets
leaving my computer go through. Next run "iptables -I INPUT -j NFQUEUE --queue-num 0". so we can trap all incoming
and outgoing packets in the queue.

delete ip table we created at end - "iptables --flush"

capture the request packets from client and save to a queue using iptables and modify then send packets
convert the raw packet to scapy packet to modify the request

Before installing Netfilterqueue you must have:
Python development files, Libnetfilter_queue development files and associated dependencies.
apt-get install build-essential python-dev libnetfilter-queue-dev
pip install NetfilterQueue
for python 3-3.7 do this instead "pip install NFQP3" and import this package from project settings

enable port forwarding so linux allows packets to flow through it like a router.
echo 1 > /proc/sys/net/ipv4/ip_forward
linux has this disabled as a security feature, so if we don't do this the victim
will lose its network connection. If the intercepted data packets are not forwarded, 
but are instead discarded, ARP spoofing can result in a denial of service (DoS).
