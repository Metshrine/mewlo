"""
manager.py

A base class for high-level site-helping managers.
"""






class MewloManager(object):
    """Base class for high-level site-helping managers; base class does little."""

    def __init__(self, mewlosite, debugmode):
        self.mewlosite = mewlosite

    def prestartup_register_dbclasses(self, mewlosite, eventlist):
        """Called before starting up, to ask managers to register any database classes BEFORE they may be used in startup."""
        pass

    def startup(self, eventlist):
        """Startup everything."""
        self.mewlosite.logevent("Startup of manager ({0}).".format(self.__class__.__name__))

    def poststartup(self, eventlist):
        """Called after startup."""
        pass

    def shutdown(self):
        """Shutdown everything, we are about to exit."""
        self.mewlosite.logevent("Shutdown of manager ({0}).".format(self.__class__.__name__))
        pass



    def dumps(self, indent=0):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        outstr = " "*indent + "MewloManager (" + self.__class__.__name__ + ") reporting in.\n"
        return outstr