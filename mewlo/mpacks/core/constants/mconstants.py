"""
mconst.py
This module contains constants used accross modules.
It provides a central place for constants so that they are easier to locate.

It's written as a class just to make the syntax of manipulating values a little cleaner.
"""


# mewlo imports


# python imports
import logging




class MewloConstants(object):


    # settings
    DEF_SETTINGSEC_config = 'config'
    DEF_SETTINGSEC_aliases = 'aliases'
    DEF_SETTINGSEC_packs = 'packs'
    DEF_SETTINGSEC_database = 'database'
    DEF_SETTINGSEC_mail = 'mail'
    #
    DEF_SETTINGNAME_pkgdirimps_sitempacks = 'pkgdirimps_sitempacks'
    DEF_SETTINGNAME_controllerroot = 'controllerroot'
    DEF_SETTINGNAME_siteurl_relative = 'siteurl_relative'
    DEF_SETTINGNAME_siteurl_absolute = 'siteurl_absolute'
    DEF_SETTINGNAME_sitefilepath = 'sitefilepath'
    DEF_SETTINGNAME_default_logfilename = 'logfilename'
    DEF_SETTINGNAME_logfilepath = 'logfilepath'
    DEF_SETTINGNAME_dbfilepath = 'dbfilepath'
    DEF_SETTINGNAME_siteview_filepath = 'siteviewpath'
    DEF_SETTINGNAME_sitename = 'sitename'
    DEF_SETTINGNAME_flag_importsetuptoolspacks = 'flag_importsetuptoolspacks'
    #
    DEF_SETTINGNAME_isenabled = 'isenabled'
    DEF_SETTINGNAME_isonline = 'isonline'
    DEF_SETTINGNAME_offline_mode = 'offline_mode'
    DEF_SETTINGNAME_offline_message = 'offline_message'
    DEF_SETTINGNAME_offline_allowadmin = 'offline_allowadmin'
    #
    DEF_SETTINGVAL_default_logfilename_defaultvalue = '${logfilepath}/mewlo.log'
    DEF_SETTINGVAL_default_pack_settings = { 'enabled': False }
    DEF_SETTINGVAL_flag_importsetuptoolspacks = True


    # site state for debugging
    DEF_SITESTATE_INITIALIZE_START = 'initializing'
    DEF_SITESTATE_INITIALIZE_END = 'initialized'
    DEF_SITESTATE_STARTUP_START = 'starting'
    DEF_SITESTATE_STARTUP_END = 'started'
    DEF_SITESTATE_SHUTDOWN_START = 'shuttingdown'
    DEF_SITESTATE_SHUTDOWN_END = 'shutdown'


    # verifications
    DEF_VFTYPE_userfield_verification = 'VFTYPE_userfield_verification'
    DEF_VFTYPE_pre_user_verification = 'VFTYPE_pre_user_verification'
    DEF_VFTYPE_userfield_verification = 'VFTYPE_userfield_verification'
    DEF_VFTYPE_user_passwordreset = 'VFTYPE_user_passwordreset'


    # package stuff
    DEF_PACK_filepatternsuffix = 'mpack'
    DEF_PACK_subdirlist = ['mpacks']
    #
    DEF_PACK_INFOFIELD_isrequired = 'isrequired'
    DEF_PACK_INFOFIELD_requires = 'requires'
    DEF_PACK_INFOFIELD_uniqueid = 'uniqueid'
    DEF_PACK_INFOFIELD_requiredpacks = 'packs'
    DEF_PACK_INFOFIELD_codefile = 'codefile'
    DEF_PACK_INFOFIELD_codeclass = 'codeclass'
    DEF_PACK_INFOFIELD_url_version = 'url.version'
    DEF_PACK_INFOFIELD_url_download = 'url.download'
    DEF_PACK_INFOFIELD_version = 'version'
    DEF_PACK_INFOFIELD_versiondate = 'versiondate'
    DEF_PACK_INFOFIELD_versioncritical = 'versioncritical'


    # forms
    DEF_FORM_GenericErrorKey = ''


    # logging
    DEF_LOG_TARGET_filemode_default = 'a'
    DEF_LOG_SqlAlchemyLoggerName = 'sqlalchemy'


    # events
    DEF_EVENT_fieldname_safelist = ['type', 'msg', 'exp', 'request', 'traceback', 'statuscode', 'loc', 'source', 'timestamp']
    #
    DEF_EVENT_TYPE_debug = 'DEBUG'
    DEF_EVENT_TYPE_info = 'INFO'
    DEF_EVENT_TYPE_warning = 'WARNING'
    DEF_EVENT_TYPE_error = 'ERROR'
    DEF_EVENT_TYPE_critical = 'CRITICAL'
    DEF_EVENT_TYPE_failure = 'FAILURE'
    DEF_EVENT_TYPE_exception = 'EXCEPTION'
    #
    DEF_EVENT_TYPE_PYTHONLOGGING_MAP = {
        'DEBUG' : logging.DEBUG,
        'INFO' : logging.INFO,
        'WARNING' : logging.WARNING,
        'ERROR' : logging.ERROR,
        'CRITICAL' : logging.ERROR,
        'FAILURE' : logging.ERROR,
        'EXCEPTION' : logging.ERROR,
        }
    DEF_EVENT_TYPE_PYTHONLOGGING_REVERSEMAP = {
        logging.DEBUG : 'DEBUG',
        logging.INFO : 'INFO',
        logging.WARNING : 'WARNING',
        logging.ERROR : 'ERROR'
        }


    # navnodes
    DEF_NAV_cache_keyname = 'navnodecache'







