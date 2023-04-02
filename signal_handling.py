
import signal
import sys
from torHandler import TorHandler

class SignalHandler:

   def onKill(signum, frame) -> None:
      print("Received kill signal")
      print("Exiting...")
      TorHandler.turnOffTor()
      sys.exit(0)

   def onInterrupt(signum, frame) -> None:
      print("Received interrupt signal")
      print("Exiting...")
      TorHandler.turnOffTor()
      sys.exit(0)

   def onExit(signum, frame) -> None:
      pass
   
   def run() -> None:
      # covering all signals
      signal.signal(signal.SIGINT, SignalHandler.onInterrupt)
      signal.signal(signal.SIGTERM, SignalHandler.onKill)
      signal.signal(signal.SIGQUIT, SignalHandler.onKill)
      signal.signal(signal.SIGHUP, SignalHandler.onKill)
      signal.signal(signal.SIGUSR1, SignalHandler.onKill)
      signal.signal(signal.SIGSEGV, SignalHandler.onKill)
      signal.signal(signal.SIGUSR2, SignalHandler.onKill)
      signal.signal(signal.SIGPIPE, SignalHandler.onKill)
      signal.signal(signal.SIGALRM, SignalHandler.onKill)
      signal.signal(signal.SIGTERM, SignalHandler.onKill)
      signal.signal(signal.SIGUSR1, SignalHandler.onKill)
      
      
    