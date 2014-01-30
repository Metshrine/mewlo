"""
testsite1.py
This class defines a test site (and will run a debug test of it if started as main script)
"""



# Mewlo imports
from mewlo.mpackages.core.site.msitemanager import MewloSiteManager
from mewlo.mpackages.core.site.msite import MewloSite
from mewlo.mpackages.core.controller.mcontroller import MewloController
from mewlo.mpackages.core.controller.mcontroller_staticfiles import MewloController_StaticFiles
from mewlo.mpackages.core.route.mroute import *
from mewlo.mpackages.core.route.mroute_staticfiles import MewloRoute_StaticFiles
from mewlo.mpackages.core.navnode.mnav import NavNode, NavLink
from mewlo.mpackages.core.database import mdbmodel_log
from mewlo.mpackages.core.eventlog.mlogtarget_database import MewloLogTarget_Database
from mewlo.mpackages.core.setting.msettings import MewloSettings
from mewlo.mpackages.core.eventlog.mlogger import MewloLogger
from mewlo.mpackages.core.eventlog.mlogtarget_file import MewloLogTarget_File
from mewlo.mpackages.core.eventlog.mlogtarget_python import MewloLogTarget_Python
from mewlo.mpackages.core.eventlog.mevent import EWarning
#
from mewlo.mpackages.site_addons.account import msiteaddon_account


# python imports
import os, sys
import logging




# Import the "mpackages" import which is just a subdirectory where the extensions specific to the site live;
# this is just a way to get the relative directory easily, and we use this in config settings
import mpackages as pkgdirimp_sitempackages
import controllers as pkgdirimp_controllers




# the test1 demo site class
class MewloSite_Test1(MewloSite):

    def __init__(self, debugmode, commandlineargs):
        # call parent constructor
        super(MewloSite_Test1, self).__init__(__name__, debugmode, commandlineargs)



    def add_settings_early(self):
        """
        This is called by default by the base MewloSite as the first thing to do at startup;
        here we expect to set some site settings that might be used early during startup.
        """

        # config settings
        config = {
            # some generic settings for every site, to point to location of some stuff
            MewloSettings.DEF_SETTINGNAME_pkgdirimps_sitempackages: [pkgdirimp_sitempackages],
            MewloSettings.DEF_SETTINGNAME_controllerroot: pkgdirimp_controllers,
            MewloSettings.DEF_SETTINGNAME_sitefilepath: os.path.dirname(os.path.realpath(__file__)),
            # should we also load mewlo site installed setuptools plugins
            MewloSettings.DEF_SETTINGNAME_flag_importsetuptoolspackages: True,
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_config, config)

        # config settings
        config = {
            # Name of site
            MewloSettings.DEF_SETTINGNAME_sitename: 'Mewlo',
            # Specify where this site serves from
            # these siteurls should not end in / so if you are serving a site at root just use relative of '' and absolute of 'http://sitename.com'
            MewloSettings.DEF_SETTINGNAME_siteurl_relative: '',
            MewloSettings.DEF_SETTINGNAME_siteurl_absolute: 'http://127.0.0.1:8080',
            #MewloSettings.DEF_SETTINGNAME_siteurl_relative: '/public/publicity',
            #MewloSettings.DEF_SETTINGNAME_siteurl_absolute: 'http://127.0.0.1:8080/public/publicity',
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_config, config)

        # config settings
        config = {
            # online status information
            MewloSettings.DEF_SETTINGNAME_isenabled: True,
            MewloSettings.DEF_SETTINGNAME_isonline: True,
            MewloSettings.DEF_SETTINGNAME_offline_mode: 'maintenance',
            MewloSettings.DEF_SETTINGNAME_offline_message: 'We are down for leap-year maintenance; we will be back soon.',
            MewloSettings.DEF_SETTINGNAME_offline_allowadmin: False,
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_config, config)


        # config some aliases we can use (for example in our templates)
        aliases = {
            # let's add an alias to where we are going to serve static files from (note this is pointing not to a directory but to a ROUTE path)
            'staticurl': '${siteurl_relative}/static',
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_aliases, aliases)


        # extension package config -- we need to explicitly enable plugins
        packageconfig = {
            'mouser.mewlotestplug' : {
                'isenabled': True,
                },
            'mouser.testpackage' : {
                'isenabled': True,
                },
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_packages, packageconfig)


        # database config
        databaseconfig = {
            'settings' : {
                'sqlalchemy_loglevel' : logging.NOTSET,
                #'sqlalchemy_loglevel' : logging.INFO,
                },
            'default' : {
                'url' : 'sqlite:///${dbfilepath}/mewlo_testsite1.sqlite',
                'table_prefix': 'mewlo_',
                'flag_echologging' : False,
                },
            'mysql_unused' : {
                # Sample configuration for mysql
                'url' : 'mysql://mewlo_user:mewlo_pass@localhost:3306/mewlo_testsite1',
                'table_prefix': 'mewlo_'
                },
            }
        self.settings.merge_settings_key(MewloSettings.DEF_SECTION_database, databaseconfig)










    def add_loggers(self):
        """This is called by default by the base MewloSite near startup, to add loggers to the system."""

        # create a single logger (with no filters); multiple loggers are supported because each logger can have filters that define what this logger filters out
        logger = self.add_logger(MewloLogger('mytestlogger'))

        # now add some targets (handlers) to it
        logger.add_target(MewloLogTarget_File(filename=self.resolve('${logfilepath}/testlogout1.txt'), filemode='w'))

        if (False):
            # want to test raising an exception on failure to write/open file? uncomment this -- the bad blank filename will throw an exception
            logger.add_target(MewloLogTarget_File(filename=''))

        if (True):
            # let's add standard python logging as a test, and route that to file; this creates a standard python-style logger and catches events sent to that
            import logging
            pythonlogger = MewloLogTarget_Python.make_simple_pythonlogger_tofile('mewlo', self.resolve('${logfilepath}/testlogout_python.txt'))
            logger.add_target(MewloLogTarget_Python(pythonlogger))
            # and then as a test, let's create an error message in this log
            pythonlogger.error("This is a manual python test error.")

        if (True):
            # let's add a database logger
            logger.add_target(MewloLogTarget_Database(baseclass=mdbmodel_log.MewloDbModel_Log, tablename='log'))





    def add_routes(self):
        """This is called by default by the base MewloSite near startup, to add routes to the system."""

        # create a routegroup
        routegroup = MewloRouteGroup()
        # overide the parent import-package-directory for the urls in this group? if we don't it will use the controller root set in SITE config
        # routegroup.set_controllerroot(pkgdirimp_controllers)

        routegroup.append(
            MewloRoute(
                id = 'home',
                path = "/",
                controller = MewloController(function='requests.request_home')
                ))


        routegroup.append(
            MewloRoute(
                id = 'hello',
                path = '/test/hello',
                args = [
                        MewloRouteArgString(
                            id = 'name',
                            required = True,
                            help = "name of person to say hello to",
                            ),
                        MewloRouteArgInteger(
                            id = 'age',
                            required = False,
                            help = "age of person (optional)",
                            defaultval = 44,
                            )
                        ],
                controller = MewloController(function="requests.request_sayhello"),
                # we can pass in any extra data which will just be part of the route that can be examined post-matching
                extras = { 'stuff': "whatever we want" },
                # we can force the route to simulate as if certain url call args were assigned (this works whether there are RouteArgs for these or not; no type checking is performed on them)
                forcedargs = { 'sign': u"aries" },
                ))



        from controllers import requests
        routegroup.append(
            MewloRoute(
                id  = 'article',
                path = '/article',
                args = [
                        MewloRouteArgString(
                            id = 'title',
                            required = False,
                            positional = True,
                            help = "title of article to display",
                            )
                        ],
                # another way to specify the controller is to pass in the actual function reference (rather than as a string)
                controller = MewloController(function=requests.request_article),
                ))

        routegroup.append(
            MewloRoute(
                id = 'help',
                path = '/user/help',
                controller = MewloController(root=pkgdirimp_controllers, function='requests.request_help'),
                ))
        routegroup.append(
            MewloRoute(
                id = 'contact',
                path = '/help/contact',
                # we can pass the root package to the MewloController constructor, which has the benefit of doing the import immediately and raising exception if not found; otherwise the error will come up during preparation
                controller = MewloController(root=pkgdirimp_controllers, function='requests.request_contact'),
                ))
        routegroup.append(
            MewloRoute(
                id = 'about',
                path = '/help/about',
                # we can pass the root package to the MewloController constructor, which has the benefit of doing the import immediately and raising exception if not found; otherwise the error will come up during preparation
                controller = MewloController(root=pkgdirimp_controllers, function='requests.request_about'),
                ))


        #static file server
        routegroup.append(
            MewloRoute_StaticFiles(
                id  = 'static_files',
                path = '/static',
                controller = MewloController_StaticFiles(
                    sourcepath = '${sitefilepath}/public_html'
                    ),
                ))


        # add routegroup we just created to the site
        self.comp('routemanager').append(routegroup)









    def add_navnodes(self):
        """Create navigational structure for site pages."""

        # these are related to Routes above, except that NavNodes are like a hierarchical menu structure / site map, wheras Routes are flat patterns that map to controllers
        nodes = [
            NavNode('home', {
                'menulabel': '${sitename} home page',
                'menulabel_short': 'home',
                'children': [],
                'parent': 'site',
                'sortweight': 1.0,
                'menuhint' : 'Return to the home page'
                }),
            NavNode('help', {
                'parent': 'site',
                'sortweight': 10.0,
                }),
            NavNode('contact', {
                'parent': 'help',
                'sortweight': 8.0,
                }),
            NavNode('about', {
                'parent': 'help',
                'sortweight': 9.0,
                }),
            ]

        # add nodes to site
        self.comp('navnodemanager').add_nodes(nodes)








    def add_addons(self):
        """Add any site addons."""
        # Add login site addon
        siteaddon = msiteaddon_account.MewloSiteAddon_Account()
        self.comp('siteaddonmanager').append(siteaddon)





























    def pre_runroute_callable(self, route, request):
        """This is called by default when a route is about to be invoked.  Subclassed sites can override it."""

        #request.logevent(EInfo("pre_runroute_callable Request URL: {0} from {1}.".format(request.get_full_path(), request.get_remote_addr())))
        # ATTN: test, let's trigger a signal
        if (False):
            id = 'signal.site.pre_runroute'
            message = {'route':route}
            source = None
            flag_collectresults = True
            signalresults = self.comp('signalmanager').broadcast(id, message, request, source, flag_collectresults)
        return None



    def post_runroute_callable(self, request):
        """This is called by default after a route has been invoked.  Subclassed sites can override it."""

        #request.logevent(EWarning("This is a test warning called POST run route: " + request.get_path()))
        return None
















































def main():
    """This function is invoked by the python interpreter if this script itself is executed as the main script."""

    # custom commandline args (if we dont have any we can pass None instead of parser to do_main_commandline_startyp()).
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--querytests", help="run some test queries",action="store_true", default=False)

    # Create a site manager and ask it to instantiate a site of the class we specify, and handle some generic commandline options
    # it returns parsed commandline args so we can look for any custom ones
    args, sitemanager = MewloSiteManager.do_main_commandline_startup(MewloSite_Test1, parser)

    # on successful creation, we can parse and do some stuff
    if (sitemanager != None):
        # sitemanager was created and early commandline processing done
        # now we have some custom commandline arg proessing we might want to do
        if (sitemanager.is_readytoserve()):
            # this stuff only is entertained if sitemanager says all green lights
            if (args.querytests):
                # simulate some simple simulated query requests
                print "Running query tests."
                print sitemanager.test_submit_path('/')
                print sitemanager.test_submit_path('/help/about')
                print sitemanager.test_submit_path('/page/mystery')
                print sitemanager.test_submit_path('/test/hello/name/jesse/age/44')

        # now any late generic commandline stuff (including serving the website)
        sitemanager.do_main_commandline_late()


if __name__ == '__main__':
    main()


