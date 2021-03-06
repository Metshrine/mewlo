Error Handling Discussion
=========================


In particular, we want to answer questions like:

    * When should we use exceptions vs error return values or tuples?
    * When and how do we log serious errors -- where in the exception chain?



Error/Exception approaches:
---------------------------

If we have a function that we expect may encounter an error, there are several ways we might handle it:

1. Getting an error description from a procedure that doesn't normally return a value (blank errorstring if no error):
errorstring = runfunction()

2. Getting an error description in addition to a return value, by returning a tuple (blank errorstring if no error):
(value, errorstring) = runfunction()

3. Using an exception to signal an error:
try:
    value = runfunction()
Exception exp:
    errorstring = str(exp)

In above cases we could use a custom error class instead of errorstring, or a custom exception, to pass additional info (see below).

In many languages, raising exceptions is very costly, but in python it's cheap and encouraged.



Different kinds of errors/exceptions:
-------------------------------------

Let us consider two kinds of "errors/exceptions".

    * The first kind of error/exception we will call "Serious Errors".  These are the kind that reflects a programming mistake or an unanticipated error that reflects a "serious" problem -- one that should be logged and where an administrator needs to be informed.  It would be common for such errors to terminate the associated request immediately without continuing.
    * The second kind of error/exception we will call "Casual Errors".  These are errors that can be considered an alternate-form of the return value from a function.  Such return values do not signify a programming error or serious problem that requires termination of the request, etc.  The programming logic by definition will take into account such error return values.
    * Another example of the casual errors are form processing errors, for which there may be multiple and they are reported with context when presenting form.


And somewhere between these two are some other things:

    * Cases where we want to log some unusual event, even if we don't technically consider it an error.
    * Cases where we want to create a "report" of warnings+errors after doing some operation or performing some validation.


So we can break this orthogonally into several dimensions:

    * How do we REPORT the "error/exception" back to our caller?
    * What kind of "object" is the error/exception?
    * How (and how far) do we propagate it up the call stack?
    * How/when do we log it?


Other issues:
    * There are a few additional interesting issues in handling "errors".
    * One issue is the case where we get an exception/error and we want return it up the chain of calls while accumulating the errors -- and to be able to report the CHAIN of exceptions (exception locations, etc.).
    * A related issue is where we may actually have multiple "errors" that we want to accumulate (possibly with some additional warnings that are possibly only relevant IF there are errors).
    * Another issue is where we need to add some context to an error/exception before processing it, perhaps to give it some additional context, etc.


Our strategy:
    * We want to use a consistent approach to error return values, exceptions, and logging.  So would should that approach be?



First draft proposal:
---------------------

    * Use formal exceptions in all cases where there is normally a return value; do not use tuples
    * Use a custom exception class to wrap all errors/exceptions, which will support adding contextual information and logging.
    * Pass exceptions up the call stack chain until they get to a "natural" place to recover; use philosophy of database transactions -- roll back until its safe to do additional work.  Often this will mean rolling back to processing of the url request and displaying an error page.
    * If a function is re-raising the objection as-is, it need not worry about logging it or converting(wrapping) it.  Only when an exception/error is consumed must the function allow it to be logged.
    * MewloRequest objects will have a ErrorTracker object attached to them which can hold multiple errors added to the request as it is processed.  In this way we can defer displaying errors until final page rendering.
    * This is similar in spirit to the way multiple form processing errors are accumulated and prepared for display.  Perhaps we can unify these concepts.
    * WHENEVER a function call could conceivably throw an exception, it should be placed in a TRY EXCEPT block, even if the only command in the except block is a raise; this is to ensure we have exceptions occuring only where we expect them.


Experience trying the first draft:
----------------------------------

This approach worked, but had some real drawbacks:
    * Python treats many programming errors as runtime exceptions, including syntax errors in code.
    * Because of this, one has to be very careful when using exceptions to catch function return-code information that is not a critical error.
    * This fundamental tension between critical exceptions and simple "failure return codes" is what makes this approach most unpleasing.
    * Having caught an exception deep in a call stack, if we want to ADD extra info to it (contextual text hints for example), we need to wrap the exception and re-raise it.
    * This does help us with issue#1 because we can use a flag in our wrapped exception to signify when it's a return-code type exception.


Second draft proposal:
----------------------

    * NEVER use exceptions for failure return codes.  Only use an exception if the event is so serious that we know the caller will not know how to handle our return code or we want immediate program halt.
    * Due to #1, all functions that might possibly return a failure message needs to return a tuple if it is a function that normally returns a value, or have the sole return value be the failure message.
    * As convention, the variable holding the "failure" message should be called "failure", and should be set to None when the function has completed with success.
    * So for example: (sum,failure) = compute_sum(a,b,c)
    * Or: failure = performoperation()
    * When the operation succeeds, failure must be returned as None; and on error it must be non-None.
    * But what kind of non-None value should be returned as failure?
    * In the most trivial scenario, where the called function KNOWS that the caller does not intend to log or report the failure, or distinguish between different kinds of failures, it is allowable to simply return boolean True value as the failure.
    * In all other cases, the convention should be to return an instance of the Event class.  There are several helper functions for creating such Event objects, including helper functions to create an Event object from an exception, recording a full traceback log of where the error occurred.
    * Event objects are fairly lightweight by default but can support arbitrary extra data using a dictionary, and are designed to be written out to log files, displayed on screen, etc. 


Experience trying the second draft:
-----------------------------------

    * The convention/approach has absolute minimal impact on performance/memory on succeess, or on trivial failure return values.
    * The convention allows arbitrary objects to be used as failure codes, BUT proscribes a standard failure object that is flexible and not too heavy.
    * The prescribed failure object can support additional features that are useful like being able to save traceback callstack information, etc.
    * The prescribed failure object is a member of the class of objects used for logging, so it is ready-made for logging and debug display.


Issues:
-------

    * We do not ENFORCE the requirement that all failure codes be Events, which could result in misuse.  We could overcome this by insisting that ALL failure return values are EITHER None or an Event.
    * Our current implementation of the Event class is purely as an open-ened dictionary, without dedicated properties.  This means that when creating new events with unusual dictionary keys for certion properies (like "level" for severity level), the possibility of a typo being uncaught is high.
    * The use of a pure dictionary-based approach to saving event properties also means the construction looks a bit messier.  e.g. instead of Event("my message",level=10) we have Event("my message",{"level":10}).
    * We could solve this by going back to a fixed set of real properties, but we did that previously, and dropped it in favor of the dictionary because the number of properties in worst case was getting large and heavyweight for cases where they weren't needed.
    * A compromise might be some optionally enabled check on dictionary key names that could be run when debugging mode is enabled.
    * Another partial solution is we can always use helper functions that take specific named parameters as options and construct Event object dynamically from them; the existing EError(), EWarning(), EException, etc functions are examples of exactly this.
    * Conclusion: Second draft is a winner.



Another benefit of using a class to represent all failure return codes is that we can easily enable a debugging feature during testing that
logs ALL such failure return code generation.
