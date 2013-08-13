"""
package.py
Works with packagemanager.py to support our package/extension/addon system
"""



# python imports
import json
import os

# helper imports
from ..event.event import EventList, EFailure

# mewlo imports
from mewlo.mpackages.core.mexception import mreraise
from mewlo.mpackages.core.mewlomisc import readfile_asjson





class Package(object):
    """
    The Package is a class represents a dynamically found module that can be used as an addon package.
    """

    def __init__(self, packagemanager, filepath):
        # keep pointer to package manager
        self.packagemanager = packagemanager
        # found info (json) file defining the package
        self.infofilepath = filepath
        # dictionary acquired from info file
        self.infodict = None
        # imported module of code
        self.codemodule_path = ""
        self.codemodule = None
        self.packageobject = None
        # last error, for debug display
        self.readytoloadcode = False
        self.readytorun = False
        self.enabled = False
        self.eventlist = EventList()



    def load_infofile(self):
        """Load the info file (json data) for this package."""

        # init
        self.infodict = None
        self.readytoloadcode = False

        # read the json file and parse it into a dictionary
        self.infodict, failure = readfile_asjson(self.infofilepath,"Package info file")
        if (failure==None):
            # set readytoloadcode true since the json parsed properly
            self.readytoloadcode = True
        else:
            # failed; add the error message to our eventlist, and continue with this package marked as not useable
            self.eventlist.add(failure)



    def load_codemodule(self):
        """Import the codemodule associated with this package."""

        # init
        self.codemodule = None
        self.codemodule_path = ""
        self.packageobject = None
        self.readytorun = False
        self.enabled = False

        # get path to code module
        self.codemodule_path, failure = self.get_pathtocodemodule()
        if (failure==None):
            # ask package manager to load the import from the path
            self.codemodule, failure = self.packagemanager.loadimport(self.codemodule_path)

        if (failure==None):
            # if the import worked, instantiate the package object from it
            failure = self.instantiate_packageobject()

        if (failure==None):
            # success so mark it as ready to run
            self.readytorun = True
            self.enabled = True
        else:
            # failed; add the error message to our eventlist, and continue with this package marked as not useable
            self.eventlist.add(failure)



    def get_pathtocodemodule(self):
        """The info file for the package should tell us what module file to import; we default to same name as info file but with .py"""
        # default module name
        path = self.infofilepath
        dir, fullname = os.path.split(path)
        name, ext = os.path.splitext(fullname)
        pathtocodemodule_default = name + ".py"
        # override with explicit
        pathtocodemodule = dir + "/" + self.get_infofile_property("codefile",pathtocodemodule_default)
        # return it
        return pathtocodemodule, None



    def instantiate_packageobject(self):
        """Assuming we have imported the dynamic package module, now create the package object that we invoke to do work"""
        # init
        packageobj = None
        # module loaded in memory?
        if (self.codemodule == None):
            return EFailure("No code module imported to instantiate package object from")
        # object class defined in info dictionary?
        packageobject_classname = self.get_infofile_property("codeclass",None)
        if (packageobject_classname == None):
            return EFailure("Package info file is missing the 'codeclass' property which defines the class of the MewloPackage derived class in the package module")
        # does it exist
        if (not packageobject_classname in dir(self.codemodule)):
            return EFailure("Package class ("+packageobject_classname+") not found in package module ("+self.codemodule.__name__+")")
        # instantiate it
        try:
            packageobj_class = getattr(self.codemodule, packageobject_classname)
            packageobj = packageobj_class(self)
        except:
            return EFailure("Package class object ("+packageobject_classname+") was found in package module, but could not be instantiated.")
        # save it for use
        self.packageobject = packageobj
        # no failure returns None
        return None



    def get_infofile_property(self, propertyname, defaultval):
        """Lookup property in our info dict and return it, or defaultval if not found."""
        if (self.infodict==None):
            return defaultval
        if (propertyname in self.infodict):
            return self.infodict[propertyname]
        return defaultval



    def update_queue_check(self):
        """Update: check online for new version. ATTN: UNFINISHED."""
        pass

    def update_queue_download(self):
        """Update: download a downloaded new version. ATTN: UNFINISHED."""
        pass

    def update_queue_install(self):
        """Update: install a new version. ATTN: UNFINISHED."""
        pass



    def debug(self,indentstr=""):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        outstr = indentstr+"Package reporting in.\n"
        indentstr += " "
        #
        outstr += self.eventlist.debug(indentstr)+"\n"
        #
        outstr += indentstr+"Info dictionary ("+self.infofilepath+"):\n"
        jsonstring = json.dumps(self.infodict, indent=12)
        outstr += indentstr+" '"+jsonstring+"'\n"
        #
        outstr += indentstr+"Code Module file: "+self.codemodule_path+"\n"
        #
        outstr += indentstr+"Code module: "
        outstr += str(self.codemodule)+"\n"
        #
        outstr += indentstr+"Package object: "
        outstr += str(self.packageobject)+"\n"
        if (self.packageobject):
            outstr += self.packageobject.debug(indentstr+" ")
        #
        return outstr

