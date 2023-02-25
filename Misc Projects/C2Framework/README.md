# C2 Framework
This set of files was built as a basic C2 framework for a college project. It is built on Python and consists of a server, client, and keylogger class file. 

## How it Works

The backdoor works in a reverse shell configuration, where the server must be running before the client can connect. Sockets are constructed for each and could be
modified to include encryption of some kind, but for now it is just encoded. Once both systems are running, a user can open a shell, run a keylogger, dump the keylogger
cache, and remove the keylog file. This set of programs is essentially a backbone from which a full platform could be built. 

This program should not be used for any illicit purpose or anything other than an educational project. 
