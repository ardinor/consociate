from consociate.consociate import CiscoHost, Consociate
from getpass import getpass


def hostPrompt(consociate, host):

    prompt = "{}> ".format(host.host)

    while 1:
        cmd = input(prompt).lower()
        
        if cmd == "print":
            pass
        
        elif cmd == "help" or cmd == "?":
            print("""
exit - exits this host prompt
            """)
        elif cmd == "exit" or cmd == "quit":
            print("Exiting...")
            break        


def mainPrompt():

    consociate = Consociate()

    print("To begin create at least one host `create host` or `import hosts`. For help, type help, to exit, type exit")
    
    while 1:
        cmd = input("> ").lower()
        if cmd == "create host":
            print("Hostname or IP address")
            hostname = input("> ")
            print("Are login details required to connect to this host?")
            loginReq = input("[Y/n]> ").lower()
            if loginReq == "n":
                pass
            else:
                print("What is the username?")
                username = input("> ")
                print("What is the password?")
                password = getpass("> ")
            print("Is an enable password set on the host?")
            enablePassReq = input("[Y/n]> ").lower()
            if enablePassReq == "n":
                pass
            else:
                print("What is the enable password?")
                enablePass = getpass("> ")
                
            print("How do you connect to the host?")
            connType = input("[SSH/telnet]> ").lower()
            if connType == "":
                connType = "ssh"
            newHost = CiscoHost(hostname, connType)
            
            consociate.addHost(newHost)
            print("Finished adding host {}".format(hostname))
            
        elif cmd[:5] == "host ":
            host = consociate.getHost(cmd[5:])
            if host:
                hostPrompt(consociate, host)
            else:
                print("Error: No host found with hostname {}!".format(cmd[5:]))
            
        elif cmd == "help" or cmd == "?":
            print("""
create host - creates a single host in a guided interview format
import hosts - imports a list of hosts from a file
list hosts - list the hosts that have been created or imported
exit - exit the application
            """)
            
        elif cmd == "exit" or cmd == "quit":
            print("Exiting...")
            break

if __name__ == "__main__":
    mainPrompt()