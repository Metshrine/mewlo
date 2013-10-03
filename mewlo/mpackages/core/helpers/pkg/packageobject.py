"""
packagepbject.py
Works with packagemanager.py to support our package/extension/addon system
"""





class PackageObject(object):
    """
    The PackageObject class is the parent class for the actual 3rd party class that will be instantiated when a package is LOADED+ENABLED.
    ATTN: UNFINISHED
    """

    def __init__(self, package):
        self.package = package



    def startup(self):
        """Do any startup stuff."""
        return None

    def shutdown(self):
        """Do any shutdown stuff."""
        return None




    def checkusable(self):
        """
        Check if this package object is actually able to run, before startup is called.
        This is where we might check any more detailed prerequisited, and check if a database update is required first.
        :return: None if all is good and its runable, or failure event if not.
        """
        return None


    def generate_admin_menu(self):
        """
        Here we want to return a list of update choices to present the user.
        ATTN: TODO - figure out the format of how to return this information.
        The idea would be to basicall return a dynamically list of menu items with attributes, so maybe something like:
            return [
                    {
                    'name': 'install',
                    'label': 'Install this addon',
                    'description': 'Run the installation script for this plugin, install database tables, etc.',
                    'auto-update': False,
                    'important': True,
                    },
                    {
                    'name': 'update',
                    'label': 'Update database for this addon',
                    'description': 'Upgrade from v1.0 to v2.02 (will modify tables x,y,z); perform a backup first! Read more at http://www.donationcoder.com',
                    'auto-update': True,
                    'important': True,
                    }
                ]
        Then the user could trigger these items interactively from a pacakge administration page, or possibly the system could run the items marked as 'auto-update' automatically.
        Note that this function is called after the system is initialized and while it is starting up, so we have access to settings and databases, etc.
        So this would be a place where we could check if we need a database update or install.
        """
        return None


    def invoke_admin_menuitem(self, admin):
        """
        We are invoking one of the items returned from generate_admin_menu function; we will be passed the dictionary of the list item selected.
        :return: None on success, or failure event if not.
        """
        return None



    def dumps(self, indent=0):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        outstr = " "*indent + "Base PackageObject reporting in.\n"
        return outstr


