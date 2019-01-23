"""
    Flask-Classful
    --------------

    Class based views for the Flask microframework.

    :copyright: (c) 2013 by Freedom Dumlao.
    :license: BSD, see LICENSE for more details.
"""

import sys
import functools
import inspect
from uuid import UUID
from werkzeug.routing import parse_rule
from flask import request, make_response
from flask.wrappers import ResponseBase
import re

_py2 = sys.version_info[0] == 2

__version__ = "0.14.2"


def route(rule, **options):
    """A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """

    def decorator(f):
        # Put the rule cache on the method itself instead of globally
        if not hasattr(f, '_rule_cache') or f._rule_cache is None:
            f._rule_cache = {f.__name__: [(rule, options)]}
        elif f.__name__ not in f._rule_cache:
            f._rule_cache[f.__name__] = [(rule, options)]
        else:
            f._rule_cache[f.__name__].append((rule, options))

        return f

    return decorator


class FlaskView(object):
    """Base view for any class based views implemented with Flask-Classful. Will
    automatically configure routes when registered with a Flask app instance.
    """

    decorators = []
    representations = {}
    route_base = None
    route_prefix = None
    trailing_slash = True
    excluded_methods = []  # specify the class methods to be explicitly excluded from routing creation
    # TODO(hoatle): make method_dashified=True as default instead,
    # this is not a compatible change
    method_dashified = False
    special_methods = {
        "get": ["GET"],
        "put": ["PUT"],
        "patch": ["PATCH"],
        "post": ["POST"],
        "delete": ["DELETE"],
        "index": ["GET"],
    }
    # supported type hints used to determine url variable converters
    type_hints = {
        str: 'string',
        int: 'int',
        float: 'float',
        UUID: 'uuid',
    }


    @classmethod
    def register(cls, app, route_base=None, subdomain=None, route_prefix=None,
                 trailing_slash=None, method_dashified=None, base_class=None, **rule_options):
        """Registers a FlaskView class for use with a specific instance of a
        Flask app. Any methods not prefixes with an underscore are candidates
        to be routed and will have routes registered when this method is
        called.

        :param app: an instance of a Flask application

        :param route_base: The base path to use for all routes registered for
                           this class. Overrides the route_base attribute if
                           it has been set.

        :param subdomain:  A subdomain that this registration should use when
                           configuring routes.

        :param route_prefix: A prefix to be applied to all routes registered
                             for this class. Precedes route_base. Overrides
                             the class' route_prefix if it has been set.
        :param trailing_slash: An option to put trailing slashes at the end of
                               routes without parameters.
        :param method_dashified: An option to dashify method name from
                                 some_route to /some-route/ route instead of
                                 default /some_route/
        :param base_class: Allow specifying an alternate base class for customization instead of the default FlaskView
        :param rule_options: The options are passed to 
                                :class:`~werkzeug.routing.Rule` object.
        """

        if cls is FlaskView:
            raise TypeError(
                "cls must be a subclass of FlaskView, not FlaskView itself")

        if not base_class:
            base_class = FlaskView

        if route_base:
            cls.orig_route_base = cls.route_base
            cls.route_base = route_base

        if route_prefix:
            cls.orig_route_prefix = cls.route_prefix
            cls.route_prefix = route_prefix

        if not subdomain:
            if hasattr(app, "subdomain") and app.subdomain is not None:
                subdomain = app.subdomain
            elif hasattr(cls, "subdomain"):
                subdomain = cls.subdomain

        if trailing_slash is not None:
            cls.orig_trailing_slash = cls.trailing_slash
            cls.trailing_slash = trailing_slash

        if method_dashified is not None:
            cls.orig_method_dashified = cls.method_dashified
            cls.method_dashified = method_dashified

        members = get_interesting_members(base_class, cls)

        for name, value in members:
            proxy = cls.make_proxy_method(name)
            route_name = cls.build_route_name(name)
            try:
                if hasattr(value, "_rule_cache") and name in value._rule_cache:
                    for idx, cached_rule in enumerate(value._rule_cache[name]):
                        rule, options = cached_rule
                        rule = cls.build_rule(rule)
                        sub, ep, options = cls.parse_options(options)

                        if not subdomain and sub:
                            subdomain = sub

                        if ep:
                            endpoint = ep
                        elif len(value._rule_cache[name]) == 1:
                            endpoint = route_name
                        else:
                            endpoint = "{0!s}_{1:d}".format(route_name, idx)
                        # print '1 - {0!s}'.format(rule)
                        app.add_url_rule(
                            rule, endpoint, proxy,
                            subdomain=subdomain, **options)

                elif name in cls.special_methods:
                    methods = cls.special_methods[name]

                    rule = cls.build_rule("/", value)
                    if not cls.trailing_slash and rule != '/':
                        rule = rule.rstrip("/")
                    elif cls.trailing_slash is True and rule.endswith('/') is False:
                        rule = '{0!s}/'.format(rule)
                    # print '2 - {0!s}'.format(rule)
                    app.add_url_rule(
                        rule, route_name, proxy,
                        methods=methods, subdomain=subdomain, **rule_options)

                else:
                    methods = getattr(cls, 'default_methods', ["GET"])

                    if cls.method_dashified is True:
                        name = _dashify_underscore(name)

                    route_str = '/{0!s}/'.format(name)
                    if not cls.trailing_slash:
                        route_str = route_str.rstrip('/')
                    rule = cls.build_rule(route_str, value)
                    if cls.trailing_slash is True and rule.endswith('/') is False:
                        rule = '{0!s}/'.format(rule)
                    # print '3 - {0!s}'.format(rule)
                    app.add_url_rule(
                        rule, route_name, proxy, subdomain=subdomain,
                        methods=methods, **rule_options)
            except DecoratorCompatibilityError:
                raise DecoratorCompatibilityError(
                    "Incompatible decorator detected on {0!s} in class {1!s}"
                    .format(name, cls.__name__))

        if hasattr(cls, "orig_route_base"):
            cls.route_base = cls.orig_route_base
            del cls.orig_route_base

        if hasattr(cls, "orig_route_prefix"):
            cls.route_prefix = cls.orig_route_prefix
            del cls.orig_route_prefix

        if hasattr(cls, "orig_trailing_slash"):
            cls.trailing_slash = cls.orig_trailing_slash
            del cls.orig_trailing_slash

        if hasattr(cls, "orig_method_dashified"):
            cls.method_dashified = cls.orig_method_dashified
            del cls.orig_method_dashified

    @classmethod
    def parse_options(cls, options):
        """Extracts subdomain and endpoint values from the options dict and returns
           them along with a new dict without those values.
        """
        options = options.copy()
        subdomain = options.pop('subdomain', None)
        endpoint = options.pop('endpoint', None)
        return subdomain, endpoint, options,

    @classmethod
    def make_proxy_method(cls, name):
        """Creates a proxy function that can be used by Flasks routing. The
        proxy instantiates the FlaskView subclass and calls the appropriate
        method.

        :param name: the name of the method to create a proxy for
        """

        i = cls()
        view = getattr(i, name)

        # Since the view is a bound instance method,
        # first make it an actual function
        # So function attributes work correctly
        def make_func(fn):
            @functools.wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        view = make_func(view)

        # Now apply the class decorator list in reverse order
        # to match member decorator order
        if cls.decorators:
            for decorator in reversed(cls.decorators):
                view = decorator(view)

        @functools.wraps(view)
        def proxy(**forgettable_view_args):
            # Always use the global request object's view_args, because they
            # can be modified by intervening function before an endpoint or
            # wrapper gets called. This matches Flask's behavior.
            del forgettable_view_args

            if hasattr(i, "before_request"):
                response = i.before_request(name, **request.view_args)
                if response is not None:
                    return response

            before_view_name = "before_" + name
            if hasattr(i, before_view_name):
                before_view = getattr(i, before_view_name)
                response = before_view(**request.view_args)
                if response is not None:
                    return response

            response = view(**request.view_args)
            code, headers = None, None

            if isinstance(response, tuple):
                response, code, headers = unpack(response)

            if not isinstance(response, ResponseBase):

                if not bool(cls.representations):
                    # representations is empty, then the default is to just
                    # output what the view function returned as a response
                    response = make_response(response, code, headers)
                else:
                    # Return the representation that best matches the
                    # representations in the Accept header
                    resp_representation = request.accept_mimetypes.best_match(
                        cls.representations.keys())

                    if resp_representation:
                        response = cls.representations[
                            resp_representation
                        ](response, code, headers)
                    elif 'flask-classful/default' in cls.representations:
                        response = cls.representations['flask-classful/default'](
                            response, code, headers
                        )
                    else:
                        # Nothing adequate found, return what the view function
                        # gave us for predictability
                        response = make_response(response, code, headers)

            # If the header or code is set, regenerate the response
            elif any(x is not None for x in (code, headers)):
                # A response can be passed into `make_response` and it will set
                # the key appropriately
                response = make_response(response, code, headers)

            after_view_name = "after_" + name
            if hasattr(i, after_view_name):
                after_view = getattr(i, after_view_name)
                response = after_view(response)

            if hasattr(i, "after_request"):
                response = i.after_request(name, response)

            return response

        return proxy

    @classmethod
    def build_rule(cls, rule, method=None):
        """Creates a routing rule based on either the class name (minus the
        'View' suffix) or the defined `route_base` attribute of the class

        :param rule: the path portion that should be appended to the
                     route base

        :param method: if a method's arguments should be considered when
                       constructing the rule, provide a reference to the
                       method here. arguments named "self" will be ignored
        """

        rule_parts = []

        if cls.route_prefix:
            rule_parts.append(cls.route_prefix)

        route_base = cls.get_route_base()
        if route_base:
            rule_parts.append(route_base)
        if len(rule) > 0:  # the case of rule='' empty string
            rule_parts.append(rule)
        ignored_rule_args = ['self']
        if hasattr(cls, 'base_args'):
            ignored_rule_args += cls.base_args

        if method and getattr(cls, 'inspect_args', True):
            argspec = get_true_argspec(method)
            args = argspec[0]
            query_params = argspec[3]  # All default args should be ignored
            annotations = getattr(argspec, 'annotations', {})
            for i, arg in enumerate(args):
                if arg not in ignored_rule_args:
                    if not query_params or len(args) - i > len(query_params):
                        # This isn't optional param, so it's not query argument
                        rule_part = "<{0!s}>".format(arg)
                        if not _py2:
                            # in py3, try to determine url variable converters
                            # from possible type hints
                            type_str = cls.type_hints.get(annotations.get(arg))
                            if type_str:
                                rule_part = "<{}:{}>".format(type_str, arg)
                        rule_parts.append(rule_part)
        result = "/{0!s}".format("/".join(rule_parts))
        return re.sub(r'(/)\1+', r'\1', result)

    @classmethod
    def get_route_base(cls):
        """Returns the route base to use for the current class."""

        if cls.route_base is not None:
            route_base = cls.route_base
            base_rule = parse_rule(route_base)
            # see: https://github.com/teracyhq/flask-classful/issues/50
            if hasattr(cls, 'base_args'):
                # thanks to: https://github.com/teracyhq/flask-classful/pull/56#issuecomment-328985183
                cls.base_args = list(set(cls.base_args).union(r[2] for r in base_rule))
            else:
                cls.base_args = [r[2] for r in base_rule]
        else:
            route_base = cls.default_route_base()

        return route_base.strip("/")

    @classmethod
    def default_route_base(cls):

        if cls.__name__.endswith("View"):
            route_base = _dashify_uppercase(cls.__name__[:-4])
        else:
            route_base = _dashify_uppercase(cls.__name__)

        return route_base

    @classmethod
    def build_route_name(cls, method_name):
        """Creates a unique route name based on the combination of the class
        name with the method name.

        :param method_name: the method name to use when building a route name
        """
        return cls.__name__ + ":{0!s}".format(method_name)


def _dashify_uppercase(name):
    """convert somethingWithUppercase into something-with-uppercase"""
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')  # better to define this once
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1-\2', name)
    return all_cap_re.sub(r'\1-\2', s1).lower()


def _dashify_underscore(name):
    """convert something_with_underscore into something-with-underscore"""
    return '-'.join(re.split('_', name))


def get_interesting_members(base_class, cls):
    """Returns a list of methods that can be routed to"""

    base_members = dir(base_class)
    predicate = inspect.ismethod if _py2 else inspect.isfunction
    all_members = inspect.getmembers(cls, predicate=predicate)
    return [member for member in all_members
            if not member[0] in base_members
            and (
                (hasattr(member[1], "__self__")
                 and not member[1].__self__ in inspect.getmro(cls))
                if _py2 else True
            )
            and not member[0].startswith("_")
            and not member[0].startswith("before_")
            and not member[0].startswith("after_")
            and not member[0] in cls.excluded_methods]


def get_true_argspec(method):
    """
    Drills through layers of decorators attempting to locate the actual argspec
    for the method.
    """

    try:
        argspec = inspect.getfullargspec(method)
    except AttributeError:
        argspec = inspect.getargspec(method)

    args = argspec[0]
    if args and args[0] == 'self':
        return argspec
    if hasattr(method, '__func__'):
        method = method.__func__
    if not hasattr(method, '__closure__') or method.__closure__ is None:
        raise DecoratorCompatibilityError

    closure = method.__closure__
    for cell in closure:
        inner_method = cell.cell_contents
        if inner_method is method:
            continue
        if not inspect.isfunction(inner_method)\
           and not inspect.ismethod(inner_method):
            continue
        true_argspec = get_true_argspec(inner_method)
        if true_argspec:
            return true_argspec


def unpack(value):
    """Return a three tuple of data, code, and headers"""
    if not isinstance(value, tuple):
        return value, 200, {}

    try:
        data, code, headers = value
        return data, code, headers
    except ValueError:
        pass

    try:
        data, code = value
        return data, code, {}
    except ValueError:
        pass

    return value, 200, {}


class DecoratorCompatibilityError(Exception):
    pass
