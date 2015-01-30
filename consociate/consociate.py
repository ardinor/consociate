import telnetlib
import time
import re

from paramiko import SSHClient, AutoAddPolicy


class Consociate():

    def __init__(self):
        self.hosts = []

    def addHost(self, host):
        self.hosts.append(host)

    def getHost(self, hostname):
        for host in self.hosts:
            if host.host == hostname:
                return host
        return None

    def getHosts(self):
        return self.hosts

    def deleteHost(self, hostname):
        for host in self.hosts:
            if host.host == hostname:
                self.hosts.remove(host)
                return True
        return False


class CiscoHost():

    def __init__(self, host, connType):
        self.host = host
        if connType != "ssh" and connType != "telnet":
            raise Exception("Invalid Connection Type...")
        self.connType = connType

        self.loginUsername = ""
        self.loginPassword = ""
        self.enablePassword = ""

    def setLoginDetails(self, username, password, enablePassword):
        self.loginUsername = username
        self.loginPassword = password
        self.enablePassword = enablePassword

    def __repr__(self):
        return "<Host:{}>".format(self.host)

    def connTypeTelnet(self):
        if self.connType == "telnet":
            return True
        return False

    def connTypeSSH(self):
        if self.connType == "ssh":
            return True
        return False

    def getUsername(self):
        if self.loginUsername:
            return self.loginUsername
        return "Not set"

    def getEnablePassSet(self):
        if self.enablePassword:
            return "Y"
        return "N"

    def getConnType(self):
        return self.connType

    def connWriteString(self, wString):
        # Since strings in Python3 are utf-8 by default we need to encode
        # it to ascii before sending it
        return wString.encode('ascii') + b"\n"

    def getResultFromCommand(self, command):

        if connTypeTelnet:
            telnetConn = telnetlib.Telnet(self.host)
            telnetConn.read_until(b"Username: ")
            telnetConn.write(self.connWriteString(self.loginUsername))
            telnetConn.read_until(b"Password: ")
            telnetConn.write(self.connWriteString(self.loginPassword))

            hostName = telnetConn.read_until(b">").decode('ascii')
            hostName = hostName.strip()[:-1]

            telnetConn.write(b"en\n")
            telnetConn.read_until(b"Password: ")
            telnetConn.write(self.connWriteString(self.enablePassword))
            telnetConn.read_until(hostname.encode('ascii') + b"#")

            # Disable paging, so no --More--, just spit it all out
            #telnetConn.write(self.connWriteString('terminal length 0'))

            result = ''

            telnetConn.write(self.connWriteString(command))

            while 1:
                time.sleep(1)  # fine tune this?
                bufferText = telnetConn.read_very_eager().decode('ascii')
                bufferText = bufferText[bufferText.find("\n"):]

                if "--More--" in bufferText:
                     bufferText = bufferText[:bufferText.rfind("\n")]
                     result += bufferText
                     telnetConn.write(chr(32))  # simulate SPACE press
                else:
                    result += bufferText
                    break

            telnetConn.write(self.connWriteString("exit"))

            result = result[:result.rfind("\n")]
            result = result.strip()

            return result

        else:
            client = SSHClient()
            # Try to load known hosts from the user's local known hosts file
            client.load_system_host_keys()
            # If it's a client we don't already have their host on file, add it
            client.set_missing_host_key_policy(AutoAddPolicy())

            client.connect(self.host, username=self.loginUsername,
                           password=self.loginPassword)

            conn = client.invoke_shell()
            conn.send(self.connWriteString('en'))
            time.sleep(.2)
            if self.enablePassword:
                conn.send(self.connWriteString(self.enablePassword))
                time.sleep(.2)

            # Disable paging, so no --More--
            conn.send(self.connWriteString('terminal length 0'))
            time.sleep(.2)

            # Clear the buffer
            conn.send(self.connWriteString(''))
            while conn.recv_ready():
                result = conn.recv(1000)

            conn.send(self.connWriteString(command))
            time.sleep(.5)
            result = ''
            while conn.recv_ready():
                result += conn.recv(1000)

            conn.send(self.connWriteString('exit'))

            result = result[result.find(command) + len(command):]
            result = result[:result.rfind("\n")]
            result = result.strip()

            return result

    def parseLogForACLs(self, log):
        logEntries = log.split('\n')
        permittedEntries = {}
        deniedEntries = {}

        for logEntry in logEntries:
            # TO DO:
            # what about the mentions of Vlans in the log entry?
            # 111.111.111.111(111) (Vlan1 0000.0c20e.b87b) -> 192.168.25.13(11111)
            # Get datetime out of it too
            # What about the number of packets at the end?
            # 192.168.25.13(11111), 1 packet
            match = re.search('list (?P<list>(\S*)) (?P<action>(permitted|denied)) (?P<protocol>(tcp|udp)) (?P<sourceIP>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))\\((?P<sourcePort>(\d+))\\) -> (?P<destinationIP>(\d+\\.\d+\\.\d+\\.\d+))\\((?P<destinationPort>(\d+))\\)', logEntry)
            if match:
                accessList = match.group('list')
                action = match.group('action')
                protocol = match.group('protocol')
                sourceIP = match.group('sourceIP')
                sourcePort = match.group('sourcePort')
                destinationIP = match.group('destinationIP')
                destinationPort = match.group('destinationPort')

                if action == 'permitted':
                    if accessList in permittedEntries.keys():
                        permittedEntries[accessList] += [{'protocol': protocol,
                                                        'sourceIP': sourceIP,
                                                        'sourcePort': sourcePort,
                                                        'destinationIP': destinationIP,
                                                        'destinationPort': destinationPort}]
                    else:
                        permittedEntries[accessList] = [{'protocol': protocol,
                                                        'sourceIP': sourceIP,
                                                        'sourcePort': sourcePort,
                                                        'destinationIP': destinationIP,
                                                        'destinationPort': destinationPort}]
                elif action == 'denied':
                    if accessList in deniedEntries.keys():
                        deniedEntries[accessList] += [{'protocol': protocol,
                                                        'sourceIP': sourceIP,
                                                        'sourcePort': sourcePort,
                                                        'destinationIP': destinationIP,
                                                        'destinationPort': destinationPort}]
                    else:
                        deniedEntries[accessList] = [{'protocol': protocol,
                                                        'sourceIP': sourceIP,
                                                        'sourcePort': sourcePort,
                                                        'destinationIP': destinationIP,
                                                        'destinationPort': destinationPort}]


