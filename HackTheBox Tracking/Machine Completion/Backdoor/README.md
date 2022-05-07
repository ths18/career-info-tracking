# Backdoor Machine Writeup

This machine was a lot of fun and it showed me that I'm getting more comfortable and learning from some previous experience. Sticking with the theme I have, there were still some setbacks, and of course they were my own doing. I got started with this machine about a month ago, and a week after starting, I was doing the NCL Team Game and while attempting some registry forensics, I totaled the windows installation on my laptop, which had all my HTB screenshots and progress. Long story short, now my laptop has arch linux! 

Moving forward, I was able to finish this machine relatively quickly. It took me about 2 weeks, but I did the bulk of the work in one day and the other time was spent doing assorted schoolwork or going to my paying job. Now, let's get into the process!

## Step 1: Recon

In the usual fashion, I started this encounter doing some recon. I alwayus start my recon off with a trusty intense scan

    nmap -T4 -A -v 10.10.11.125 
