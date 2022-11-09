import socket
from IPy import IP

class PortScan():
    def __init__(self, tgt, ports):
        """ 
        Constructor. Initialize the PortScan with the passed input values and set the class variables accordingly.
        """
        self.target = tgt
        self.port = ports

    def scan(self):
        #enumerate through range 1 to number_of_ports + 1. Since this port scan started at 1, it made sense to go 1 past the requested number.
        #invoke the scantarget function and pass the port parameter
        print('\nScanning target: ' + str(self.target))
        for port in range(1, int(self.port)+1):
            self.scanTarget(port)

    def check_ip(self, ip):
        """
        This function is intended to check the IP or host name that was given before passing it forward
        """
        try:
            return (IP(self.target))
        except ValueError:
            return(socket.gethostbyname(ip)) # if a hostname is given, the function recovers the IP and returns
    
    def get_banner(self, s):
        """ This function just recieves whatever data the TCP request responds with, giving us our banner"""
        return s.recv(1024) 

    def scanTarget(self, port):
        """
         This function is called by the earlier scan function. 
         The goal is to take the port that was passed, construct a socket, and connect to the socket and the given port.
        """
        modified_ip = self.check_ip(self.target)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
            s.settimeout(1.0)      # invoke the timeout function. Shorter timeout results in faster scans at the possible cost of accuracy
            s.connect((modified_ip, port))  # invoke the connect method and pass the converted_ip and port parameters
            try:
                banner = self.get_banner(s)
                print("   Port " + str(port) + " is open: " + banner.decode())
            except:
                print('   Port ' + str(port) + ' is open :')
            sock.close()
        except:
            #print('   Port ' + str(port) + ' is closed') Commented out since we do not want to see every single failure
            pass

targets_ip = input('Enter target to scan for open ports : ')
number_of_ports = input('How many ports do you want to scan? Enter number here : ')

myPortScan = PortScan(targets_ip, number_of_ports)
myPortScan.scan()