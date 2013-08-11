"""
debugging.py
This module contains miscelaneous functions that aid debugging and logging and error reporting.
"""





def smart_dotted_idpath(obj):
    """
    We try to get a nice dotted path for an object, by assuming it has attribute accessor functions of get_parent and get_id
    We walk up parent path (as far as we are able) and return a dotted path string.
    This function depends on the convention of the object methods get_parent and get_id.
    When there is no get_parent we stop traveling up chaing.
    When there is no get_id we simply use class name.
    """

    retstr = ''
    while (True):
        # get the name of this object itself (or fallback to class name), and add it to the dotted string so far
        objidstr = smart_dotted_idpath_getobjidstr(obj)
        if (retstr==''):
            retstr = objidstr
        else:
            retstr = objidstr + "."+ retstr
        # lookup the parent object if it has one
        obj = smart_dotted_idpath_getparentobj(obj)
        if (obj == None):
            # stop when there is no more parent in the chain
            break
    # return the built string
    return retstr



def smart_dotted_idpath_getobjidstr(obj):
    """Interal use function.  Return the nice idstr for the object; fall back on classname if needed."""

    # class name
    classname = obj.__class__.__name__

    # find the get_id attribute func
    try:
        getidfunc = getattr(obj, "get_id")
        if (getidfunc and callable(getidfunc)):
            # ok we found a get_id function, so invoke it and get id string
            objid = getidfunc()
            if (objid!=classname):
                return classname+"("+objid+")"
    except:
        # not an error, just drop down
        pass
    # fallback on class name
    return classname


def smart_dotted_idpath_getparentobj(obj):
    """Interal use function.  Return the parent object of this object, IFF we can find a get_parent function to call; otherwise return None"""

    # find the get_parent attribute func
    try:
        getparentfunc = getattr(obj, "get_parent")
        if (getparentfunc and callable(getparentfunc)):
            # ok we found a get_parent function so get the parent object from it
            return getparentfunc()
    except:
        # not an error; just drop down
        pass
    # not found
    return None









