Usually people don't type https while typing url, and sends http request to server. The webserver 
then sends back a response (if webserver allows https) asking the user to communicate over 
https instead.

The hacker in the middle, using SSLstrip, can detect that server is asking to upgrade the
connection, and strip all fileds/data that asks the user to upgrade. So the https response is
stripped down to normal http. So now victim does not get to know that server allows https, and
will again send next request as normal http. But SSLstrip keeps track of servers that want to
communicate over https, so when user sends http request, it upgrades it to https, keeping the
server happy, and the victim blindsided. So webserver communicates over https with the manin
the middle hacker, thinking of it as the client. SSLstrip also converts all links on the 
loaded page from https to http. HSTS can be used to overcome such MITM attacks.

sslstrip acts as an intermediary between victim and server.

flow:   	client ---->sslstrip(hacker) ----->server
request:	http ------>https----------------->server
respond:	http<-------https<-----------------server

if it does not work, clear the cache on the web browser and try again.

Steps: 

run an arp_spoof on your desired target machine to become MITM

open a terminal on hacker machinne and run "sslstrip" 
#sslstrip runs on port 10000 by default and only analyzes the packets that pass through it, ignores rest
# we need to redirect all packets coming on port80 to port 10000

run "iptables -I OUTPUT -j NFQUEUE --queue-num 0" this is the chain where packets
leaving my computer go through. Next run "iptables -I INPUT -j NFQUEUE --queue-num 0". so we can trap all incoming
and outgoing packets in the queue.

#write a iptables rule to sslstrip as a proxy from client to server so sslstrip sit as intermeditate to modify the data
# modify table nat, append prerouting rule to table, apply to tcp packets that go/come from port 80, redirect to 1000
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

# delete ip table we created at end - "iptables --flush"

run fileInterceptor or codeInjector script to do some attacks on target machine. dport and sport are changed to 10000.


