
from pathlib import Path
import subprocess


class TorHandler:

    __defaultport: int = 9050
    torPort: int = __defaultport

    #tor configuration to be written to torrc
    torrcConfiguration: str = """

    """    
    #setting the tor port to change torrc file
    def setPort(portNumber) -> None:
        TorHandler.torPort = portNumber

    #starting tor as a service with brew
    def startTor() -> int:
        torCommand: exec = subprocess.run("brew services start tor".split(" "))
        return torCommand.returncode

    #start running traffic through tor network
    def configureSocks5proxy() -> int:
        startConfig: exec = subprocess.run("sudo networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9050 off".split(" "))
        finishConfig: exec= subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi on".split(" "))
        return startConfig.returncode and finishConfig.returncode

    ############################# Curently working here
    def configureTorSettings() -> str:
        
        torrcFilePathOnMac: str = "/usr/local/etc/tor/torrc"
        torrcMacGhostBackup: str = "/usr/local/etc/tor/torrc.macghost"

        torrcFileExist: bool = Path(torrcFilePathOnMac).is_file()
        backupFileExist: bool = Path(torrcMacGhostBackup).is_file()
        
        #creating backup file for torrc 
        if(torrcFileExist):
            
            if(not backupFileExist):
                subprocess.run("mv {} {}".format(torrcFilePathOnMac,torrcMacGhostBackup))

            with open(torrcFilePathOnMac, 'w') as torrcFile:
                torrcFile.write(TorHandler.torrcConfiguration)
                torrcFile.close()
        
    
    def checkIfTorIsWorking() -> int:
        checkTor: exec= subprocess.run("curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/".split(" "))
        return checkTor.returncode
    
    def turnOffTor() -> None:
        #disable traffic running through tor first so no issues occur when tor is turned off
        turnOffTorFirewall: exec = subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi off".split(" "))
        #completely turn off the tor daemon
        turnOffTor: exec = subprocess.run("brew services tor stop".split(" "))
