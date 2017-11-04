import launcher
import os
import logging
import sys

def startRPC(self, port, eventListenerPort):
  
  logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)
  reqOS = ["darwin", "win32", "windows", "linux"]
  reqArch = ["x64", "ia32"]
  cfg = launcher.Config(reqOS, reqArch);
  launcherLocal = launcher.launcher()
  # define log file name for rpc agent, so e.g
  # for "runConsumerOWP.py" it will be: "rpc-wpwithin-runConsumerOWP.log"
  logfilename = os.path.basename(sys.argv[0])
  logfilename = "rpc-wpwithin-" + logfilename.rsplit(".", 1)[0] + ".log"

  args = []
  if eventListenerPort > 0:
    logging.debug(str(os.getcwd()) + "" + "-port " + str(port) + " -logfile " + logfilename + " -loglevel debug,warn,error,fatal,info" + " -callbackport " + str(eventListenerPort))
    args = ['-port', str(port), '-logfile', logfilename, '-loglevel', 'debug,warn,error,fatal,info', '-callbackport', str(eventListenerPort)]
  else:
    logging.debug(str(os.getcwd()) + "" + "-port " + str(port) + " -logfile " + logfilename + " -loglevel debug,warn,error,fatal,info")
    args = ['-port', str(port), '-logfile', logfilename, '-loglevel', 'debug,warn,error,fatal,info']

  process = launcherLocal.launch(cfg, os.getcwd() + "", args)
  
  return process

def stopRPC(self, process):
  print "Will try and stop RPC service"
  process.kill()