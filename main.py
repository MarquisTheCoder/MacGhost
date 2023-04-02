
import signal
from torHandler import TorHandler
from commands import optHandler
import sys
import os
import time

#Written by: Deshawn Marquis Williams
    #AKA: @MarquisThecoder on github
#Date: 11DEC2022 11:15

#Reason: because I couldn't a viable alternative to torghost 
#which I used to use on my linux desktop. Also, just to make it easy
#for others to learn and do what took me a minute to find out on OSX.

#Description: MacGhost is a Tor routing application with a clean user interface to allow anyone with 
#a mac and an internet connection to route all outgoing and incoming traffic through the 
#tor routing service



def load_html(window):
    time.sleep(5)
    indexFile = open("index.html", "r")
    indexPage = indexFile.readlines()
    window.load_html(indexPage)


# root of the program
def main():

    signal.signal(signal.SIGINT, TorHandler.turnOffTor)
    signal.signal(signal.SIGTERM, TorHandler.turnOffTor)
    signal.signal(signal.SIGQUIT, TorHandler.turnOffTor)
    signal.signal(signal.SIGHUP, TorHandler.turnOffTor)
    signal.signal(signal.SIGUSR1, TorHandler.turnOffTor)
    signal.signal(signal.SIGSEGV, TorHandler.turnOffTor)
    signal.signal(signal.SIGUSR2, TorHandler.turnOffTor)
    signal.signal(signal.SIGPIPE, TorHandler.turnOffTor)
    signal.signal(signal.SIGALRM, TorHandler.turnOffTor)
    signal.signal(signal.SIGTERM, TorHandler.turnOffTor)
    signal.signal(signal.SIGUSR1, TorHandler.turnOffTor)

    # TorHandler.startTor()
    # TorHandler.configureSocks5proxy()
    TorHandler.turnOffTor()
     # print("Working dir:", os.getcwd())
    # f = open("index.html",)
    # indexPage = f.readlines()
    # f.close()

    # window = webview.create_window('Main page', html=indexPage)
    # webview.start(load_html, window)

if __name__ == '__main__':
    main() 