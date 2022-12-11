
from torHandler import TorHandler
from commands import optHandler
import webview
import sys
import os


#Written by: Deshawn Marquis Williams
    #AKA: @MarquisThecoder on github
#Date: 11DEC2022 11:15

#Reason: because I couldn't a viable alternative to torghost 
#which I used to use on my linux desktop. Also, just to make it easy
#for others to learn and do what took me a minute to find out on OSX.

#Description: MacGhost is a Tor routing application with a clean user interface to allow anyone with 
#a mac and an internet connection to route all outgoing and incoming traffic through the 
#tor routing service

def main():
    if os.geteuid() != 0:
         sys.exit("\nOnly root can run this script\n") 

    webview.create_window('MacGhost - tor routing application', width = 800, height = 500)
    webview.start()

if __name__ == "__main__":
    main()