"""
mresponse.py
This file contains classes to support response to requests.
For now, our MewloResponse class is just a thin wrapper over a werkzeug response.
"""


# helper imports
from ..eventlog.mevent import EventList, EError, EWarning
from ..setting import msettings
from ..helpers import thindict

# werkzeug imports
import werkzeug
from werkzeug.wrappers import Response





class MewloResponse(object):
    """
    The MewloResponse class handles the response to a server request
    Note that our response class contains a reference to the request object.
    """

    def __init__(self, request):
        self.request = request
        self.isfinalized = False
        #
        self.wresp = None
        #
        self.statuscode = None
        #
        #self.headers = None
        self.headers = [('Content-Type', 'text/html; charset=utf-8')]
        self.responsedata = None
        self.direct_passthrough = False
        self.mimetype = None
        #
        self.eventlist = EventList()
        #
        # ATTN: ugly, why are we calling this 'context'??
        #self.context = msettings.MewloSettings()
        self.context = thindict.MThinDict()
        self.did_add_defaultcontext = False
        #
        self.pendingcookiedict = {}






    def make_werkzeugresponse(self):
        """Create a werkzeug response object and attach it to us."""
        # note if the werkzeug is already made, do nothing more, just return it
        if (self.wresp == None):
            self.wresp = Response(response=self.responsedata, status=self.statuscode, headers=self.headers, direct_passthrough=self.direct_passthrough, mimetype=self.mimetype)
            # merge pending cookies to save
            self.merge_pendingcookiedict()
        return self.wresp



    def start_and_make_wsgiref_response(self, wsgiref_start_response):
        """This is invoked when we want to send a final response to the wsgi web server."""

        # now create werkzeug response via werkzeug
        wresp = self.make_werkzeugresponse()
        # now response to wsgiref from werkzeug is to invoke the callable
        retv = wresp(self.request.get_environ(), wsgiref_start_response)
        # return it
        return retv


    def get_mewlosite(self):
        return self.request.mewlosite

    def set_status(self, statuscode):
        # set values
        self.statuscode = statuscode

    def set_status_ok(self):
        # set values
        self.statuscode = 200

    def set_headers(self, headers):
        self.headers=headers

    def set_direct_passthrough(self, direct_passthrough):
        self.direct_passthrough = direct_passthrough

    def set_mimetype(self, mimetype):
        self.mimetype = mimetype

    def set_isfinalized(self):
        self.isfinalized = True

    def add_status_error(self, statuscode, errorstr):
        # set values
        self.set_status(statuscode)
        self.eventlist.add(EError(errorstr,{'statuscode': statuscode}))

    def set_responsedata(self, responsedata, statuscode = 200):
        self.responsedata = responsedata
        self.statuscode = statuscode

    def calc_wsgiref_status_string(self):
        return str(self.statuscode)



    def set_cookieval(self, cookiename, cookieval):
        """Set cookie value."""
        if (self.wresp == None):
            # response is not created yet, save it to our internal cookie dictionary which will get copied in when wresp is created
            self.pendingcookiedict[cookiename] = cookieval
        else:
            self.wresp.set_cookie(cookiename,cookieval)

    def merge_pendingcookiedict(self):
        """Because wresp response object may not be created at time of cookie setting, we may have deferred cookie values to set when we create the wresp."""
        for key,val in self.pendingcookiedict.iteritems():
            self.wresp.set_cookie(key,val)








    def set_pageid(self, pageid):
        """Shortcut to set some context settings."""
        self.context.update({'pagenodeid':pageid})

    def add_pagecontext(self, args):
        """Shortcut to set some context settings."""
        self.context.update(args)


    def add_defaultcontext(self):
        """Add some default context."""
        # ATTN: see mtemplatehelper for some non-DRY repetition of code; improve
        mewlosite = self.get_mewlosite()
        #
        self.context['settings'] = msettings.MewloSettings()
        self.context['request'] = self.request
        self.context['response'] = self
        self.context['site'] = mewlosite
        #
        self.context['user'] = self.request.get_user_or_maketemporaryguest()
        #
        self.context['thelper'] = mewlosite.templatehelper
        self.context['alias'] = mewlosite.assetmanager.get_resolvedaliases()
        #
        self.did_add_defaultcontext = True


    def run_beforeview(self):
        """Do stuff before any views."""
        if (not self.did_add_defaultcontext):
            self.add_defaultcontext()


    def finalize_response(self):
        """
        This function is invoked after the response is finished being built and is about to be sent as a reply.
        It is responsible for final error checking, and will do things like display an error if no response has been set.
        """

        # any final error checking?
        if (self.isfinalized):
            return
        self.isfinalized = True

        if (self.eventlist.count_errors() == 0):
            # if there are no EXPLICIT errors, then we check if we need to add any
            # statuscode not set? this is an internal error
            if (self.statuscode == None):
                self.add_status_error(500, u"Response statuscode not set")
            # response data not set? this is an internal error
            if (self.responsedata == None):
                self.add_status_error(500, u"Response data not set")

        # add errors to response
        self.add_errors_to_response()




    def add_errors_to_response(self):
        """Helper funciton to add any pending accumulated errors to the response."""

        if (self.eventlist.count_errors() == 0):
            return
        rstr = str(self.eventlist)
        if (self.responsedata == None):
            self.responsedata = rstr
        else:
            self.responsedata.append(rstr)







    def render_from_template_file(self, templatefilepath, args=None):
        """Shortcut to render a template and set responsedata from it, passing response object to template as an extra arg."""
        template = self.get_mewlosite().templates.from_file(templatefilepath)
        return self.render_from_template(template, args)

    def renderstr_from_template_file(self, templatefilepath, args=None):
        """Shortcut to return html for a template and set responsedata from it, passing response object to template as an extra arg."""
        template = self.get_mewlosite().templates.from_file(templatefilepath)
        return self.renderstr_from_template(template, args)


    def render_from_template(self, template, args=None):
        """Shortcut to render a template and set responsedata from it, passing response object to template as an extra arg."""
        self.set_responsedata(self.renderstr_from_template(template,args))
        return None

    def renderstr_from_template(self, template, args=None):
        """Shortcut to return html for a template and set responsedata from it, passing response object to template as an extra arg."""
        # ATTN: TODO note we are mutating the passed args in order to add a response item -- this will be fine most of the time but we may want to copy instead
        # ATTN: TODO in future use self.context instead of make_templateargs() to remove DRY violation
        # ensure we have added default keys to response context dictionary
        self.run_beforeview()
        # now merge in any passed to us
        if (args != None):
            self.context.update(args)
        renderedtext = template.render_string(self.context)
        return renderedtext












    def serve_file_bypath(self, filepath):
        """Serve a file."""
        # guess the mimetype of the file we are serving (see http://docs.python.org/3.4/library/mimetypes.html)
        import mimetypes
        (mime_type, mime_encoding) = mimetypes.guess_type(filepath)
        self.set_mimetype(mime_type)
        # open file in BINARY mode - note that we MUST open it "rb" mode or it will fail (we leave it open, garbage collector should clean it)
        thefile = open(filepath,'rb')
        # tell werkzeug that we are using passthrough mode (important for streaming large files)
        self.set_direct_passthrough(True)
        # set the data
        self.set_responsedata(thefile)


















    def dumps(self, indent=0):
        """Return a string (with newlines and indents) that displays some debugging useful information about the object."""
        # finalize if its not finalized yet
        self.finalize_response()
        #
        outstr = " "*indent + "MewloResponse reporting in.\n"
        outstr += " "*indent + " Status: " + self.calc_wsgiref_status_string() + "\n"
        outstr += " "*indent + " Response Body: " + self.responsedata + "\n"
        return outstr



