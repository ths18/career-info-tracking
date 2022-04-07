# 'Paper' Machine Writeup/progress 

## First Attempt: Several Weeks Ago

In my first attepts and weeks of off and on effort, I ran some nmap scans and got a feel for the pentesting side of things as it was new to me. Nmap shows me there are 3 main services: 
* Openssh 8.0 Protocol 2.0: Port 22
* Apache httpd 2.4.37: Port 80 & 443

## Newest Findings: 03/20/2022

There are no major vulnerabilities in the apache server that can be exploited to my knowledge. However, this particular version has a known CVE addressing a problem with SCP allowing remote code injection. This gives me a few steps to take to successfully exploit & control this machine:
* *Step 1: Figure out how to create a shell
* *Step 2: Attach that shell with a command following this structure: scp  /sourcefile remoteserver:'`touch /tmp/exploit.sh`/targetfile'
* *Step 3: Connect to shell & escalate privileges accordingly (This is not specific yet as I am still figuring this out

### TO BE CONTINUED ...

## IMPORTANT UPDATE: 04/06/2022

After some more in depthh research, I found out I was *massively* overcomplicating this machine. I was on the right track with knowledge of this exploit, but one thing that never crossed my mind was taking a breath and taking the proper recon steps and seeing what I can find. I will be leaving the section above because being able to own your overcomplications is an important step. 

That being said, let's get into the real writeup!

### First Step: Network Recon

As always, we started this machine out with an nmap scan to see what was open. We can see the same Apache httpd and Openssh services running here.
![nmap](https://user-images.githubusercontent.com/70218428/162097263-0a7c0abd-50d7-462b-8e6d-0e26124b1218.png)

### Second Step: Exploring Findings Deeper

Since earlier attempts to enumerate and brute force SSH users did not go very well, I decided to pursue the http server a little bit more. The obvious first step here is to visit the URL, 10.10.11.143, in a web browser. I went to Chrome, pasted the link, and there was no connection. Here's where things get painfully stupid.

For my working environment, I have a windows host machine and WSL running a kali linux distro. Within WSL, I was using openvpn to connect to this machine. What I initially did not take into account was that wsl2 runs as a full virtual machine, so the network is separate too. If you do not already know or think of this, to be able to view this particular IP in a web browser, I was going to need to install an openvpn client onto my host system, OR launch WSL in the Kali Desktop Experience, and I tested both before settling on KeX.

Moving past that, entering 10.10.11.143 into the browser pulls up a nice and neat default centos apache page. Inspecting this page gives you some more stuff to play around with, including a nice little _XSS-BACKEND-SERVER_ header in the network activity. This header gives us a hint that this site commonly goes by the hostname **office.paper**. To be able to view this domain, I added 10.10.11.143  office.paper to my etc/hosts file and visited that link in a browser. This pulls us to a nice little site of a paper company mimicking _The Office_, with a beautiful little message at the bottom saying **Powered by Wordpress**

### Third Step: Dive into Wordpress

As many do, I have a love/hate relationship with wordpress. Mine comes a little more from working in a web development job and seeing these issues from the other end. In this case, I researched and found a neat tool called **WPScan**, leading me to the following command.

  > wpscan --url http://office.paper/ --enumerate u,ap

This command scans the link and enumerates the users and all installed plugins on the site, as well as the usual Wordpress information.

![WP_Scan](https://user-images.githubusercontent.com/70218428/162098623-77c4c8b7-22cc-46c1-b9f0-626271ce6c15.png)


In this case, we found some very useful information. The wordpress version here was a known-insecure version (5.2.3) with an exploit that allows any user to view draft pages without authenticating by passing a simple query string and accessing the draft directly. In this case, I was able to view a draft page with some nice and sensitive information inside. I used this exploit to craft the URL http://office.paper/?static=1. In my first use, I got the html raw using curl because I had not figured out the very simple vpn issue I listed earlier at this time. 

![curl_proof](https://user-images.githubusercontent.com/70218428/162098943-a44b0eef-7dc3-4fd9-b343-d43ce38d71cf.png)


What you can see here is that one user has posted a link meant for a private employee site, namely chat.office.paper, onto a draft page in the hope that no one would see it. Unfortunately for him, that is not the case.

### Fourth Step: Enumerate, Exploit, & Escalate

After adding chat.office.paper to etc/hosts as I did earlier, I visited it in the web browser. This takes you to a registration page asking for a name, email, and password. Upon registering, you're taken to a site that has a messaging system called RocketChat that is similar to Slack or Discord. Within the only visible channel is a bot called Recyclops, built by a user 'dwight'. Investigating a bit, it turns out that you can directly interact with recyclops and use it to navigate and view any file on the machine if you know your unix systems well enough. You can use the command ***recyclops list*** to mimic a ls command, and ***recyclops file <filename>*** to display the contents of a file. We get a few nice bits of information here.
  
To cut to the chase, I chose to get access first and do some exploring later. I used the command ***recyclops file ../../../etc/passwd*** (exact number of levels up may be +- 1, I forgot to write that number down. I was excited). The output of that showed a few users, and the one that I chose to get into was dwight, because without him we never could have made it this far. There was a directory called hubot with a file called .env, and having recyclops retrieve that gives us the password clear as day. Next up, all it took was logging in with the user 'dwight' and the password 'Queenofblad3s!23', and we had access! Within that home directory, the user flag was claimed. 
  * _For some reason, I did not take a screenshot of this_
  
One flag down, one left. Within this home directory, there was a conveniently placed CVE, which turned out to be a perfect privelege escalation script pre-prepared. It was as simple as running python3 CVE-2021-3560.py, which was a polkit exploit.
  
  ![privesc_start](https://user-images.githubusercontent.com/70218428/162101013-b27aa21f-e3b2-4566-ab6c-a26a12965517.png)

  
Once this exploit ran, a new super user called 'ahmed' was created. From there it was just as simple as running the command su ahmed, and from there stepping to sudo su, and we were at root! 
  
  ![privesc_to_root](https://user-images.githubusercontent.com/70218428/162101132-e560cd60-825b-4197-86c1-a04c308c3e91.png)

  
 From there, using cd to the root home directory uncovered the system flag, and with that the machine was defeated!
  ![owned_notif](https://user-images.githubusercontent.com/70218428/162101199-d4de2272-7efc-466e-9ac2-d5f6bee188fd.png)

  
  If you're reading this, thanks for sticking around this long and I hope you enjoyed the chaos. This was my first HTB machine attempt and many valuable lessons were learned, especially the importance of following the proper steps and not getting ahead of yourself. 
