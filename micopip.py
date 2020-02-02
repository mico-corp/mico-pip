##---------------------------------------------------------------------------------------------------------------------
##  MICO-PIP
##---------------------------------------------------------------------------------------------------------------------
##  Copyright 2020 Pablo Ramon Soria (a.k.a. Bardo91) pabramsor@gmail.com
##---------------------------------------------------------------------------------------------------------------------
##  Permission is hereby granted, free of charge, to any person obtaining a copy of this software
##  and associated documentation files (the "Software"), to deal in the Software without restriction,
##  including without limitation the rights to use, copy, modify, merge, publish, distribute,
##  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
##  furnished to do so, subject to the following conditions:
##
##  The above copyright notice and this permission notice shall be included in all copies or substantial
##  portions of the Software.
##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
##  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
##  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
##  OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
##  CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
##---------------------------------------------------------------------------------------------------------------------

from github import Github
import os
import sys
from getpass import getpass

class MicoPip:
    def __init__(self):
        self.user = input("Github User: ")
        self.pwd = getpass("Github password: ")
        self.gh = Github(self.user, self.pwd )
        self.__LoadPluginList()

        self.pluginBuildDir = home = os.path.expanduser("~")+"/.mico/plugin_build"
        if not os.path.exists(self.pluginBuildDir):
            os.makedirs(self.pluginBuildDir)

        self.flowPluginDir = home = os.path.expanduser("~")+"/.flow/plugins"
        if not os.path.exists(self.flowPluginDir):
            os.makedirs(self.flowPluginDir)

    def listPlugins(self):
        for plugin in self.plugins:
            print(plugin.name)

    def installPlugin(self, _name):
        print("[0%] Getting repository")
        os.popen("git clone https://github.com/mico-corp/"+_name+" " + self.pluginBuildDir+"/"+_name).read()
        os.popen("mkdir " + self.pluginBuildDir+"/"+_name+"/build").read()
        print("[25%] Configuring project compilation")
        os.popen("cd " + self.pluginBuildDir+"/"+_name+"/build && cmake ..").read()
        print("[50%] Compiling project")
        os.popen("cd " + self.pluginBuildDir+"/"+_name+"/build && make -j4").read()
        print("[75%] Installing library")
        os.popen("cd " + self.pluginBuildDir+"/"+_name+"/build && make flow_install").read()
        os.popen("cd " + self.pluginBuildDir+"/"+_name+"/build && sudo make install").read()
        print("[100%] finished")
        
    def existPlugin(self, _name):
        exist = False
        for plugin in self.plugins:
            if(_name == plugin.name):
                exist = True
                break
        return exist

    def promptMode(self):
        cmd = ["help"]
        while(cmd[0] != "exit"):
            if(cmd[0] == "help"):
                self.help()
            elif (cmd[0] == "list"):
                self.listPlugins()
            elif (cmd[0] == "install"):
                if(cmd[1] == "all"):
                    for plugin in self.plugins:
                        self.installPlugin(plugin.name)
                else:
                    self.installPlugin(cmd[1])
            
            cmd = input("Introduce command: ")
            cmd = cmd.split(" ")

    def __LoadPluginList(self):
        self.plugins = []
        for plugin in self.gh.get_organization("mico-corp").get_repos():
            if "mplugin" in plugin.name:
                self.plugins.append(plugin)


    def help(self):
        print("MICO pip (micopip) is a python based utility for installing MICO modules easily from command line.")
        print("Following actions can be called from this prompt:")
        print("\t - \"help\" : Show this message")
        print("\t - \"exit\" : Exit micopip")
        print("\t - \"list\" : list available modules that can be installed from this utility")
        print("\t - \"install\" [module_name]: install given module. If module_name==all, install all modules")


if __name__ == "__main__":
    pip = MicoPip()

    pip.promptMode()