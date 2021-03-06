Error Handling Policy
=====================


When Mewlo functions want to signify an error, they should so by returning an error value, either as sole return value or as a tuple.

The failure value MUST be None on success (not True or False!).

On failure, the failure value *CAN* be anything other than None, including a string describing the failure, BUT SEE NEXT SECTION FOR BEST PRACTICE.

Call examples:
    (value, failure) = myfunc(a,b)
    failure = myproc(a,b)


In the function it would look like:

def myfunc(a,b):
    # success
    return (a+b, None)
    # failure
    return (None, "bad args passed")



Best Practice:
--------------

Best practice of returning failure codes, return an Event object as a failure.

It is permissable to use any* type value for the failure return value IFF the function is basically an internal function that will be called frequently and by known callers, and utmost speed is required, or in cases where the nature of the failure will always be known and is not important.
However, the type value MUST be able to be str() for display; it is highly suggested that in cased where maxiumum efficiency is desired, a string is returned describing the failure.

In all other cases, the failure return value should derive from the Event class.
By doing so, we ensure a standard way of describing failures that makes it easy to display and log them, assign severity levels, add extra info, add call stack trace info, etc.

A simple wrapper function to create a failure event can be found in events.py, called EFailure, and is used as follows:
    return EFailure("failure message goes here.")
This wrapper function also supports additional args that can aid in debugging.



Aesthetic consistency:
----------------------

The name of the variable holding the failure value should be "failure"

After calling a function that returns a failure code, prefer checking for success first followed by error, and by writing "if failure == None:", eg.:

    failure = myproc(a,b)
    if failure == None:
        # success
        stuff to do here
    else:
        # failure
        stuff to do here

If we have a multiple step process where a failure may occur at any point, the following code flow is recommended:

    failure = myproc_step1(a,b)
    if (failure==None):
        failure = myproc_step2(a,b)
    if (failure==None):
        failure = myproc_step3(a,b)
    if (failure==None):
        failure = myproc_step4(a,b)

In this way, the failure variable holds the first error, and subsequent steps are not taken.
This is slightly less efficient than nesting the checks, but nesting makes it a bit harder to add/move code so we prefer it.




Dealing with exceptions:
------------------------

As described above, Mewlo code should normally avoid throwing exceptions; exceptions should be used only for fatal errors that we cannot anticipate.

However, we will frequently be calling functions in other modules that do throw exceptions.

Mewlo code should always try+catch such anticipateable exceptions and return failure values as described above.

A useful thing to do when catching such an exception, a frequently useful thing to do is use the helper function EException() in the events.py module to convert/wrap the exception object info a Mewlo Event object, which is the recommended object to return for failure values.
This is useful because it preserves all exception info and creates an (albeit heavyweight) failure value suitable for logging or display.

Occasionally we may want to re-raise an exception instead of returning it as a failure object.
When doing so, we may want to add info to the exception to help explain the nature/location of the exception.
To do so, use the helper function mreraise() in the mexectpion.py module.


If a function returns a failure return value, the caller is REQUIRED to check it.

If a function caller collects a failure return value, *IT* becomes responsible for handling that value -- either returning it to *IT'S* caller, or consuming it after *DEALING* with it (which may include logging, etc.)

If you consume/swallow a non-None failure code, YOU MUST ensure it is properly logged or dealt with.


NOTE: You can always do a raise ExceptionPlus(failurevalue) to raise a failure into an exception if you don't know how to deal with a non-None failure value.

When I should throw an exception?
Throw an exception if you want Mewlo to be halted immediately.
This includes, by definition, cases where the caller function does not accept or check a failure return value.



