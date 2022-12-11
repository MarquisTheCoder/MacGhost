
from torHandler import TorHandler
from commands import optHandler
import webview
import sys
import os

def main():
     if os.geteuid() != 0:
         sys.exit("\nOnly root can run this script\n") 


if __name__ == "__main__":
    main()