from consociate.consociate import CiscoHost, Consociate
from getpass import getpass


def run():

    consoc = Consociate()

    print("To begin create at least one host `create host` or `import hosts`.")
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
            print(connType)
            if connType == "":
                connType = "ssh"
            print(connType)
            print(type(connType))
            newHost = CiscoHost(hostname, connType)
            
            consoc.addHost(newHost)
            
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
    run()