"""
mverificationmanager.py
Helper for verifications data
"""


# mewlo imports
from ..manager import manager
from mverification import MewloVerification







class MewloVerificationManager(manager.MewloManager):
    """The MewloVerificationManager class helps verification management."""


    def __init__(self, mewlosite, debugmode):
        super(MewloVerificationManager,self).__init__(mewlosite, debugmode)

    def startup(self, eventlist):
        super(MewloVerificationManager,self).startup(eventlist)

    def shutdown(self):
        super(MewloVerificationManager,self).shutdown()


    def dumps(self, indent=0):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        outstr = " "*indent + "MewloVerificationManager (" + self.__class__.__name__ + ") reporting in.\n"
        return outstr
