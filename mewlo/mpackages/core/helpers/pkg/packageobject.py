# package.py
# Works with packagemanager.py to support our package/extension/addon system






class PackageObject(object):
    """
    The PackageObject class is the parent class for the actual 3rd party class that will be instantiated when a package is LOADED+ENABLED
    """

    def __init__(self, package):
        self.package = package


    def debug(self,indentstr=""):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        outstr = indentstr+"Base PackageObject reporting in.\n"
        return outstr


