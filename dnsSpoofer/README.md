The Domain Name System (DNS) is a distributed system used worldwide for translating internet
domain names into IP addresses. The DNS returns an IP address that is assigned to a specific
domain name. This process is referred to as name resolution. DNS spoofing refers to a variety
of situations in which DNS name resolution is tampered with – specifically to the IP address 
of a domain name being faked. This means that the device establishes a connection to the fake
IP address and data traffic is redirected to a fake server. A particularly insidious characteristic 
of DNS spoofing is the fact that the correct domain name is displayed in the browser. A particularly 
insidious characteristic of DNS spoofing is the fact that the correct domain name is displayed in the 
browser.

DNS Spoofer Program Strategy: First intercept packets. 3 strategies to spoof dns once
you are MITM. One approach (less programming involved) is to configure and install a 
application for DNS server on your machine similar to actual DNS server and return 
whatever request user enters. Second is to craft a dns response in hacker computer and send
back to user by changing IP to any malicious one. This requires extensive knowledge of how
DNS and network layers work. Third (this program's strategy) is to forward request to DNS server,
wait for response and modify response, only modify IP part to send back the ip we want.

