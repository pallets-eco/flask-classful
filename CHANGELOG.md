2023-09-07 F.N. Claessen <felix@seita.nl>
-----------------------------------------

    Version: 0.16.0

    - Tasks:
        * Compatibility with werkzeug 2.2 #145


2021-12-25 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.15.0-b1

    - Features:
        * Add additional init_argument to register method #86
        * Add @method decorator and handling #109

    - Improvements:
        * inspect.getargspec() is deprecated, use inspect.signature() or inspect.getfullargspec() #94

    - Tasks:
        * Bugs/fix update failed travis ci build #93
        * should use github actions to run CI checks to replace travis-ci #134


2017-10-19 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.14.1

    - Tasks:
        * should have breaking sections on changelog and migration section on docs to upgrade to v0.14, v0.11 #79


2017-10-05 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.14.0

    - Breaking Changes:
        * The behavior of the trailing slash should be more intuitive and consistent #47
        * Better representations #33 #72

    - Features:
        * Type hints support for py3 #34
        * `base_class` introduced #38
        * Add options passing to `werkzeug.Routing.Rule` from register function #46
        * Enable using custom decorators in FlaskView #29
        * Should allow specifying excluded methods from becoming routes #41

    - Improvements:
        * Better representations #33 #72
        * Docker workflow along with teracy-dev for better dev setup #32 #63 #66 #67

    - Bugfixes:
        * The behavior of the trailing slash should be more intuitive and consistent #47
        * `base_args` should not be overriden when `route_base` is set #50

    - Tasks:
        * Keep the original license #51
        * Fix docs publishing #61


Details: https://github.com/teracyhq/flask-classful/milestone/8?closed=1

2016-09-03 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.13.1

    - Bugfixes:
        * route_base and trailing_slash conflict. #31

Details: https://github.com/teracyhq/flask-classful/issues?q=milestone%3A0.13.1+is%3Aclosed


2016-07-07 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.13.0

    - Features:
        * Should support route generation configuration for dashifying method names #26

Details: https://github.com/teracyhq/flask-classful/milestone/7?closed=1


2016-07-05 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.12.0

    - Bugfixes:
        * Special methods should work with Python 3.5 type hints #25

Details: https://github.com/teracyhq/flask-classful/issues?q=milestone%3A0.12.0+is%3Aclosed


2016-05-18 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.11.0
        
    - Breaking Changes:
      * The order in which `FlaskView` decorators are applied has been reversed #49

    - Improvements:
        * enhance 3rd party decorators #14 (BREAKING CHANGES for the decorator members: reversed order)

Details: https://github.com/teracyhq/flask-classful/issues?q=milestone%3A0.11.0+is%3Aclosed

2016-05-16 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.10.0
    
    - Improvements:
        * Fix "Prefer `format()` over string interpolation operator" issue #18
    
    - Bugfixes:
        * should allows flask.jsonify to return status codes and headers #19

Details: https://github.com/teracyhq/flask-classful/issues?q=milestone%3A0.10.0+is%3Aclosed

2016-03-18 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.9.0
    
    - Improvements:
        * Rename flask-classy to flask-classful for pypi publish and development


2016-02-16 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.8.0
    
    - Improvements:
        * Use code and headers in make_response()
        * Update travis-ci build script
        * Import flask_classy instead of flask.ext.classy on docs
        * Add more tests


2016-01-15 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.7.1

    - Bugfixes:
        * Fix setup.py for the right version specification

2015-08-20 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.7.0

    - Features:
        * add representations support for better serialization

    - Improvements:
       * move some attributes, methods to outer scope for overriding

    - Bugfixes:
        * Fixes docs typos


2015-08-07 Hoat Le <hoatle@teracy.com>
--------------------------------------

    Version: 0.6.11

    - Bugfixes:
        * Fixes empty url with route decorator


2013-11-19 Freedom Dumlao <freedomdumlao@gmail.com>
---------------------------------------------------

    Version 0.6.8

    - Bugfixes:
        * Fixes an issue where before_request and before_<view> methods
          that returned responses had their responses ignored. If these
          methods return a response it will be returned to the client.

    - Thanks:
        * Thanks to reddit user akaGrim for reporting the issue!

2013-11-8 Freedom Dumlao <freedomdumlao@gmail.com>
--------------------------------------------------

    Version 0.6.7

    - Features:
        * Adds a feature that allows control over trailing slashes.


2013-10-22 Freedom Dumlao <freedomdumlao@gmail.com>
---------------------------------------------------

    Version 0.6.6

    - Bugfixes:
        * Fixes a bug introduced around certain types of decorators.
          Adds more tests for those cases as well.


2013-10-22 Freedom Dumlao <freedomdumlao@gmail.com>
---------------------------------------------------

    Version 0.6.4

    - Features:
        * Added route_prefix, a feature that allows you to
          specify a prefix for all the routes generated by
          a FlaskView instance.

    - Bugfixes:
        * Fixes some bugs related to self referential
          decorators.

    - Thanks:
        * Thanks to Stephane Rufer for the idea for
          route_prefix.


2013-6-13 Freedom Dumlao <freedomdumlao@gmail.com>
--------------------------------------------------

    Version 0.6.3

    - Features:
        * Python 3.3 and Flask 0.10 is now supported.

    - Bugfixes
        * Fixed a that would cause FlaskViews without route_base
          attributes to fail to revert to that state after
          having them registered with a route_base in the register
          method.

    - Thanks:
        * Thanks to Ivan Kleshnin, who reported the bug.

2013-6-10 Freedom Dumlao <freedomdumlao@gmail.com>
--------------------------------------------------

    Version 0.6.1

    - Bugfixes
        * Fixed a bug when raising the DecoratorCompatibilityError.

    - Thanks:
        * Thanks to Ivan Kleshnin, who found and fixed the bug.


2013-6-5 Freedom Dumlao <freedomdumlao@gmail.com>
-------------------------------------------------

    Version 0.6

    - **Breaking Changes**
        * Classmethods are filtered out when determining which methods
          should be routeable.

    - Features
        * FlaskViews now support a "decorators" attribute which takes a list
          of decorators to apply to every method in that view.
        * The route_base now supports arguments.
        (Thanks to Philip Schleihauf)



    - Bugfixes
        * Fixed a bug that prevented Flask-Classy from generating routes for
          methods that had used a decorator but did not also use the @route
          decorator.
          (Thanks to Shuhao Wu for reporting)
        * view_args dict modifications made before the FlaskView view is called
          are now available in the FlaskView.
          (Thanks to Philip Schleihauf)

    - Thanks:
        * Thanks to Max Countryman, Julien Rebetez, Philip Schleihauf, and Shuhao Wu



2012-11-29  Freedom Dumlao <freedomdumlao@gmail.com>
----------------------------------------------------

    Version 0.5.2

    - Bugfixes
        * Fixed a SyntaxError that was caused by using a dictionary generator
          in Python versions earlier than 2.7.
          (Thanks to @maxcountryman)

2012-11-20  Freedom Dumlao <freedomdumlao@gmail.com>
----------------------------------------------------

    Version 0.5.1

    - Bugfixes
        * Fixed a bug that caused views that used the @route decorator to
          ignore the subdomain keyword parameter specified in the
          FlaskView's register method.
          (Thanks to Mark Grey for reporting.)

2012-11-18  Freedom Dumlao <freedomdumlao@gmail.com>
----------------------------------------------------

    Version 0.5

    - **Breaking Changes**
        * Changed the way routes are generated to match up with Flask
          documentation. index, post and custom methods without parameters
          are still configured with a trailing slash. put, patch, get,
          delete, and custom methods with parameters are configured without
          a trailing slash now.

        * Changed the way endpoints are generated to accommodate the more
          common cases. Methods with a single route are no longer have
          endpoints suffixed with an index.
          (Thanks to Jesaja Everling for the original patch.)

    - Features
        * Added support for specifying a custom endpoint using an endpoint
          keyword argument in the @route decorator.

    - Bugfixes
        * Fixed a bug that would not allow you to use any parameter name
          but "id" in the special methods.

2012-11-11  Freedom Dumlao <freedomdumlao@gmail.com>
----------------------------------------------------

    Version 0.4.3

    - Features
        * Added wrapper methods for views

    - Bugfixes
        * Fixed a bug that caused blueprint subdomains to be ignored

2012-11-05  Freedom Dumlao <freedomdumlao@gmail.com>
----------------------------------------------------

    Version 0.4

    * Added support for subdomains

2012-11-1   Freedom Dumlao  <freedomdumlao@gmail.com>
-----------------------------------------------------

    Version 0.3.4

    * Added PATCH support
