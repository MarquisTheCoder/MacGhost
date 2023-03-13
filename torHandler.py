
import coloredlogs, logging
from pathlib import Path
import subprocess

logger = logging.getLogger(__name__)

# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
coloredlogs.install(level='DEBUG')

# If you don't want to see log messages from libraries, you can pass a
# specific logger object to the install() function. In this case only log
# messages originating from that logger will show up on the terminal.
coloredlogs.install(level='DEBUG', logger=logger)

class TorHandler:

    __defaultport: int = 9050
    torPort: int = __defaultport

    #tor configuration to be written to torrc
    torrcConfiguration: str = """
    SOCKSPort {}
    SOCKSPort 192.168.0.1:9100 
    RunAsDaemon 1    
    """.format(__defaultport)    

    #setting the tor port to change torrc file
    def setPort(portNumber) -> None:
        TorHandler.torPort = portNumber

    def getPort() -> int: 
        return TorHandler.torPort
    
    #starting tor as a service with brew
    def startTor() -> int:
        logger.info("[+] Starting the Tor Daemon process")
        torCommand: exec = subprocess.run("brew services start tor".split(" "))

        if(torCommand.returncode):
            logger.info("[+] Tor daemon started successfully")
        else:
            logger.info("[-] Tor daemon failed to start")

        return torCommand.returncode

    #start running traffic through tor network
    def configureSocks5proxy() -> int:
        logger.info("[+] Starting to configure the network firewall")
        startConfig: exec = subprocess.run("sudo networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9050 off".split(" "))
        finishConfig: exec= subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi on".split(" "))
        if(startConfig.returncode and finishConfig.returncode):
            logger.info("[+] Network firewall setup completed successfully")
        else:
            logger.info("[-] Network firewall could not be setup")

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
