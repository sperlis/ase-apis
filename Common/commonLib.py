import sys
import json

class CommonLib(object):
    # hold the execution options
    # the only mandatory fields are KeyId/KeySecret
    Options = {}

    # process the command-line options and performs the initial authorization with ASoC
    def __init__(self):
        self.getCommandLineOptions()

    # process the execution options.
    # If a config file exists it gets loaded first
    # command-line options override config file options
    # NOTE: at miniumum, config file/command line must include authorization KeyId/KeySecret
    def getCommandLineOptions(self):
        if (not self.Options):
            # read config file
            self.loadConfig()
                
            if (not "asoc" in self.Options):
                self.Options["asoc"] = {}
            if (not "ase" in self.Options):
                self.Options["ase"] = {}
            
            # process command-line. To override config file the format must be <name>=<value>
            # if explicit name is not provided to the option, a "$clp<index>" name is gerneated
            index = 0
            for val in sys.argv:
                eq = val.find('=')
                if eq == -1:
                    self.Options["$clp" + str(index)] = val
                    index += 1
                else: 
                    name = val[0:eq]
                    if (name == "KeyId" or name == "KeySecret"):
                        self.Options["asoc"][name] = val[eq+1:]
                        self.Options["ase"][name] = val[eq+1:]
                    elif (name == "Username" or name == "Password"):
                        self.Options["ase"][name] = val[eq+1:]
                    else: self.Options[val[0:eq]] = val[eq+1:]

        return self.Options
        
    def loadConfig(self):
        config = open("config.json","r")
        self.Options = json.load(config)
        config.close()

    # provides an option value given a specific name
    def Option(self, name):
        if (self.Options):
            return self.Options[name]
