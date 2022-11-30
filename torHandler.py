
import subprocess

class TorHandler:

    __defaultport: int = 9050
    torPort: int = __defaultport
    
    def setPort(portNumber) -> None:
        torPort = portNumber
    
    def startTor() -> int:
        torCommand = subprocess.run(["tor"])
        return torCommand.returncode

    
    def configureSocks5proxy() -> int:
        startConfig = subprocess.run("sudo networksetup -setsocksfirewallproxy Wi-Fi 127.0.0.1 9050 off".split(" "))
        finishConfig = subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi on".split(" "))
        return startConfig.returncode and finishConfig.returncode
    
    def configureTorrcFile() -> str:
        pass
    
    def checkIfTorIsWorking() -> int:
        checkTorCommand = subprocess.run("curl --socks5 localhost:9050 --socks5-hostname localhost:9050 -s https://check.torproject.org/".split(" "))
        return checkTorCommand.returncode

    def turnOffTor() -> int:
        turnOffTorCommand = subprocess.run("sudo networksetup -setsocksfirewallproxystate Wi-Fi off".split(" "))
        return turnOffTorCommand.returncode

    