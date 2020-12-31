2 main ways to connect between hacker and victim. 1st is to for a direct/bind
connection, where a port is opened up on victim machine to listen from hacker.
But this can be detected by firewall etc. 2nd is to form a reverse connection,
where hacker opens a port on their computer to listen for incoming connections.
Backdoor execution makes the victim connect to this port.

run "nc -vv -l -p 4444" on hacker terminal to open a port and listen for 
incoming connections. OR 

run listener2.py to listen using custom-made listener having more features like 
uploading/downloading files.