Site Addons
===========

Django has the concept of an "App" which is a moduler, reusable, self-contained set of files that implement some controller routes, views, and configuration information.
Think of an "App" like a self-contained add-on which can handle certain requests (usually matching a url prefix).

The reusable and modular nature of such bundles is what makes them appealing.

Mewlo supports such a concept.  The term "app" is misleading but i don't have a much better term at this point, so i'm just refering to them as "site addons".


Django docs on how these "apps" are self-contained:
    * https://docs.djangoproject.com/en/dev/intro/reusable-apps/ - general
    * https://docs.djangoproject.com/en/dev/ref/templates/api/#template-loaders - template treatment
    * https://docs.djangoproject.com/en/dev/intro/tutorial06/ - static file treatment
    * http://www.caktusgroup.com/blog/2013/06/12/making-your-django-app-more-pluggable/