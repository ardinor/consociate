import telnetlib
import time

class CiscoConnection():

    def __init__(self, host, connType):
        self.host = host
        if connType != "SSH" or connType != "Telnet":
            raise Exception("Invalid Connection Type...")
        self.connType = connType

        self.loginUsername = ""
        self.loginPassword = ""
        self.enablePassword = ""

    def connTypeTelnet(self):
        if self.connType == "Telnet":
            return True
        return False

    def connTypeSSH(self):
        if self.connType == "SSH":
            return True
        return False

    def telnetWriteString(self, wString):
        return wString.encode('ascii') + b"\n"

    def getResultFromShowCommand(self, command):

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



