# -*- coding: utf-8 -*-
import os
import errno

class ResourceManager:
    """
    Author: Janusz Kowalczyk
    Date  : 2013-07-13

    Simple resouce manager class.
    Instantiate it with the path to the resource folder.
    If resources_folder is ommitted then os.getcwd() is used.

    Examples:
        To retrieve a path to a file or a directory, create new object:
        RES = ResourceManager(os.path.join(os.getcwd(),"resources"))
        then use get() to retrieve full path to that file or directory
        RES.get("twimls")
    """
    def __init__(self, resources_folder=os.getcwd()):
        self.resources_folder=resources_folder

    def get(self, path):
        """
        Will return an absolute path to a requested file or directory if found
        in the configured resource folder.
        """
        if os.path.isdir(os.path.join(self.resources_folder,path)):
            print "Requested path points at a directory %s" % (os.path.join(self.resources_folder,path))
            return os.path.join(self.resources_folder,path)
        elif os.path.isfile(os.path.join(self.resources_folder,path)):
            print "Requested path points at a file %s" % (os.path.join(self.resources_folder,path))
            return os.path.join(self.resources_folder,path)
        else:
            print "Requested path '%s' doesn't exist in configured resource folder '%s' !!!" % (path, self.resources_folder)
            return None
