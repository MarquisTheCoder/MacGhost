
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
        askForPasswordUpfront: exec = subprocess.run("sudo -v".split(" "))

        # starting the tor daemon to be run in the background
        torCommand: exec = subprocess.run("brew services start tor".split(" "))

        #checking if the tor daemon started successfully
        if(torCommand.returncode):
            logger.info("[+] Tor daemon started successfully!")
        else:
            logger.info("[-] Tor daemon failed to start")

        return torCommand.returncode


    #start running traffic through tor network
    def configureSocks5proxy() -> int:
        logger.info("[+] Starting to configure the network firewall")

        #attempting to configure the network firewall to run through local proxy
        startConfig: exec = subprocess.run("sudo networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9050 off".split(" "), capture_output=True, text=True)

        # making sure that the network firewall is configured successfully and the wifi interface is up
        finishConfig: exec= subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi on".split(" "), capture_output=True, text=True)
       
       #checking the return codes of the commands above
        if(startConfig.returncode == 0 and finishConfig.returncode == 0 ):
            logger.info("[+] Network firewall setup completed successfully!")
        else:
            logger.info("[-] Network firewall could not be setup")
            print(startConfig.returncode)
            print(finishConfig.returncode)
            print(startConfig.stderr)
            print(finishConfig.stderr)

        return startConfig.returncode and finishConfig.returncode

    ############################# Curently working here

    # these commands will be used to configure the tor daemon
    # and set a backup to the original torrc file
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
        turnOffTor: exec = subprocess.run("brew services stop tor".split(" "))
