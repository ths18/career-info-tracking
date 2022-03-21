# 'Paper' Machine Writeup/progress #

## First Attempt: Several Weeks Ago##

In my first attepts and weeks of off and on effort, I ran some nmap scans and got a feel for the pentesting side of things as it was new to me. Nmap shows me there are 3 main services: 
* Openssh 8.0 Protocol 2.0: Port 22
* Apache httpd 2.4.37: Port 80 & 443

##Newest Findings: 03/20/2022 ##
There are no major vulnerabilities in the apache server that can be exploited to my knowledge. However, this particular version has a known CVE addressing a problem with SCP allowing remote code injection. 

