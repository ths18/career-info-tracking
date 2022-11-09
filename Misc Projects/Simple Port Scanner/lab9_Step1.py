import socket
from IPy import IP

def scan(target):
# enumerate through a range of ports (1 - 100)
# invoke the scanTarget function and pass the parameters
    converted_ip = check_ip(target)
    print('\nScanning target: ' + str(converted_ip))
    for port in range(1, 100):
        scanTarget(converted_ip, port)

def check_ip(ip):
    """
    This function is intended to check the IP or host name that was given before passing it forward
    """
    try:
        return (IP(ip))
    except ValueError:
        return(socket.gethostbyname(ip)) # if a hostname is given, the function recovers the IP and returns

def get_banner(s):
    # return value from s.recv() function
    """ This function just recieves whatever data the TCP request responds with, giving us our banner"""
    return s.recv(1024)

def scanTarget(ipaddress, port):
    """
    This function is called by the earlier scan function. 
    The goal is to take the port that was passed, construct a socket, and connect to the socket and the given port.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
        s.settimeout(0.75)      # invoke the timeout function. Shorter timeout results in faster scans at the possible cost of accuracy
        s.connect((ipaddress, port))  # invoke the connect method and pass the converted_ip and port parameters
        try:
            banner = get_banner(s)
            print('   Port ' + str(port) + ' is open : ' + str(banner.decode().strip('\n')))
        except:
            print('   Port ' + str(port) + ' is open : Specific Service Unknown')
        sock.close()
    except:
        #print('   Port ' + str(port) + ' is closed') Commented out since we do not want to see every single failure
        pass

def main():
    targets = input('Please input the target IP or Domain Name. For multiple, please separate by COMMA ONLY: ')
    if ',' in targets:
        for ip_add in targets.split(','):
            # invoke the scan function and pass the parameter
            scan(ip_add)
    else:
        scan(targets)

if __name__ == '__main__':
    main()