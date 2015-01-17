import telnetlib
import time

class Consociate():

    def __init__(self):
        self.hosts = []
        
    def addHost(self, host):
        self.hosts.append(host)


class CiscoHost():

    def __init__(self, host, connType):
        self.host = host
        if connType != "ssh" and connType != "telnet":
            raise Exception("Invalid Connection Type...")
        self.connType = connType

        self.loginUsername = ""
        self.loginPassword = ""
        self.enablePassword = ""
        
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

    def telnetWriteString(self, wString):
        return wString.encode('ascii') + b"\n"

    def getResultFromCommand(self, command):

        if connTypeTelnet:
            telnetConn = telnetlib.Telnet(self.host)
            telnetConn.read_until(b"Username: ")
            telnetConn.write(self.telnetWriteString(self.loginUsername))
            telnetConn.read_until(b"Password: ")
            telnetConn.write(self.telnetWriteString(self.loginPassword))

            hostName = telnetConn.read_until(b">").decode('ascii')
            hostName = hostName.strip()[:-1]

            telnetConn.write(b"en\n")
            telnetConn.read_until(b"Password: ")
            telnetConn.write(self.telnetWriteString(self.enablePassword))
            telnetConn.read_until(hostname.encode('ascii') + b"#")

            result = ''

            telnetConn.write(command.encode('ascii') + b"\n")

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

            telnetConn.write(b"exit\n")

            result = result[:result.rfind("\n")]
            result = result.strip()

            return result
