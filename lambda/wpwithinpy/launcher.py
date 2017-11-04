#!/usr/bin/python
## Python Launcher
import platform
import os
import sys
from subprocess import call
import subprocess
import logging

class Config(object):
    def __init__(self, requiredOSs, requiredArchs):
        self.requiredOSs = requiredOSs
        self.requiredArchs = requiredArchs
        # Arch can be { 'arm', 'ia32', or 'x64' } as per https://nodejs.org/dist/latest-v5.x/docs/api/process.html#process_process_arch
        # OS can be { 'darwin', 'freebsd', 'linux', 'sunos' or 'win32' } as per https://nodejs.org/dist/latest-v5.x/docs/api/process.html#process_process_platform

class launcher(object):

    def __init__(self):
        logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)
        logging.info("Initialising launcher")
        
    def launch(self, cfg, path, flags):
      logging.debug("Determine the OS and Architecture this application is currently running on")
      hostOS = platform.system().lower()
      logging.debug("hostOS: " + str(hostOS))
      is_64bits = sys.maxsize > 2**32
      if is_64bits:
          hostArchitecture = 'x64'
      else:
          hostArchitecture = 'ia32'
      logging.debug("hostArchitecture: " + str(hostArchitecture))
      if(self.validateConfig(cfg, hostOS, hostArchitecture)):
          if(hostOS == "darwin"):
              process = self.launchDarwin(path, flags)
              return process
          elif(hostOS == "linux"):
              process = self.launchLinux(path, flags)
              return process
          elif(hostOS == "win32"):
              process = self.launchWindows(path, flags)
              return process
          elif (hostOS == "windows"):
              process = self.launchWindows(path, flags)
              return process
          else:
            logging.debug("Unable to launch binary on host architecture (Unsupported by launcher)(Host=" + str(hostOS) + ")")
      else:
          logging.debug("Invalid OS/Architecture combination detected")

    def detectHostOS(self):
        """Return the operating system as 'windows', 'darwin' or 'linux'."""
        os_name = platform.system().lower()
        if os_name == 'windows' or os_name == 'darwin':
            return os_name
        else:
            return 'linux'

    def detectHostArchitecture(self):
        """Return the architecture as '386', 'amd64', 'arm32' or 'arm64'."""
        out = ''
        if platform.machine().lower()[:3] == 'arm':
            out += 'arm'
        if sys.maxsize > 2**32:
            if out == 'arm':
                out += '64'
            else:
                out = 'amd64'
        else:
            if out == 'arm':
                out += '32'
            else:
                out = '386'
        return out


    #Make it a thread!    
    def launchDarwin(self, path, flags):
        logging.info("launching Darwin application")
        if os.environ.get("WPW_HOME") is not None:
            cmd = [os.environ["WPW_HOME"]+'/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        else:
            cmd = [path + '/wpwithinpy/iot-core-component/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        cmd.extend(flags)
        proc = subprocess.Popen(cmd)
        return proc
    
    def launchLinux(self, path, flags):
        logging.info("launching Linux application")
        if os.environ.get("WPW_HOME") is not None:
            cmd = [os.environ["WPW_HOME"]+'/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        else:
            cmd = [path + '/wpwithinpy/iot-core-component/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        cmd.extend(flags)
        proc = subprocess.Popen(cmd)
        return proc
        
    def launchWindows(self, path, flags):
        logging.info("launching Windows application")
        if os.environ.get("WPW_HOME") is not None:
            cmd = [os.environ["WPW_HOME"]+'/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        else:
            cmd = [path + '/wpwithinpy/iot-core-component/bin/rpc-agent-' + self.detectHostOS() + '-' + self.detectHostArchitecture()]
        cmd.extend(flags)
        proc = subprocess.Popen(cmd)
        return proc

    def validateConfig(self, cfg, hostOS, hostArchitecture):
        logging.debug("Validate detected parameters against config")
        validOS = False;
        validArch = False;
        for indCfg in cfg.requiredOSs:
            logging.debug(str(indCfg))
            if indCfg.lower() == hostOS:
                validOS = True
        for indCfg in cfg.requiredArchs:
            logging.debug(str(indCfg))
            if indCfg.lower() == hostArchitecture:
                validArch = True
        return validOS and validArch
