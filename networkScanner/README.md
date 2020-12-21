Address Resolution Protocol (ARP) is a procedure for mapping a dynamic 
Internet Protocol address (IP address) to a permanent physical machine 
address in a local area network (LAN). The physical machine address is 
also known as a Media Access Control or MAC address. 

ARP works between network layers 2 and 3 of the Open Systems Interconnection 
model (OSI model). The MAC address exists on layer 2 of the OSI model, the 
data link layer, while the IP address exists on layer 3, the network layer.

Three of the four addresses in an ARP request packet are known: the source 
and destination IP and the source MAC.

When you try to ping an IP address on your local network, say 192.168. ... 
If there is a value cached, ARP is not used. If the IP address is not found 
in the ARP table, the system will then send a broadcast packet to the 
network using the ARP protocol to ask "who has 192.168".

arp -a          -> command shows arp table