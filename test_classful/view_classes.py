import logging
import asyncio

from flask import jsonify, request
from flask_classful import FlaskView, route, method
from functools import wraps

VALUE1 = "value1"


def get_value():
    return VALUE1


class BasicView(FlaskView):

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id, 404

    def put(self, id):
        return "Put " + id, 403, {'say': 'hello'}

    def patch(self, id):
        return "Patch " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def custom_method(self):
        return "Custom Method"

    def custom_method_with_params(self, p_one, p_two):
        return "Custom Method {0!s} {1!s}".format(p_one, p_two)

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self):
        return "Multi Routed Method"

    @route("/noslash")
    def no_slash_method(self):
        return "No Slash Method"

    @route("/endpoint/", endpoint="basic_endpoint")
    def custom_endpoint(self):
        return "Custom Endpoint"

    @route("/route3/", methods=['POST'])
    def custom_http_method(self):
        return "Custom HTTP Method"

    @method("POST")
    def methoddecorated(self):
        return request.method

    @method("POST")
    @method("PATCH")
    def methodtwicedecorated(self):
        return request.method

    @method("POST")
    @route("/methodroute")
    def methodplusroute(self):
        return request.method


class SubdomainAttributeView(FlaskView):
    subdomain = "sub1"

    def index(self):
        return "Index"


class SubdomainRouteView(FlaskView):

    @route("/", subdomain="sub2")
    def index(self):
        return "Index"


class IndexView(FlaskView):
    route_base = "/"

    def index(self):
        return "Index"


class RouteBaseView(FlaskView):
    route_base = "/base-routed/"

    def index(self):
        return "Index"

class RouteBaseViewIsNotLatest(FlaskView):
    def index(self):
        return "Index"


class RoutePrefixView(FlaskView):
    route_prefix = "/my_prefix/"

    def index(self):
        return "Index"


class VarBaseView(FlaskView):
    route_base = "/var-base-route/<route>"

    def before_index(self):
        request.view_args.pop('route')

    def index(self):
        return "Custom routed."

    def with_base_arg(self, route):
        return "Base route arg: " + route

    @route('/local/<route_local>', methods=['GET'])
    def with_route_arg(self, route, route_local):
        return "{0!s} {1!s}".format(route, route_local)


class BeforeRequestView(FlaskView):

    def before_request(self, name):
        self.response = "Before Request"

    def index(self):
        return self.response


class BeforeViewView(FlaskView):

    def before_index(self):
        self.response = "Before View"

    def index(self):
        return self.response


class BeforeRequestReturnsView(FlaskView):

    def before_request(self, name):
        return "BEFORE"

    def index(self):
        return "Should never see this"


class BeforeViewReturnsView(FlaskView):

    def before_index(self):
        return "BEFORE"

    def index(self):
        return "Should never see this"


class AfterViewView(FlaskView):

    def after_index(self, response):
        return "After View"

    def index(self):
        return "Index"


class AfterRequestView(FlaskView):

    def after_request(self, name, response):
        return "After Request"

    def index(self):
        return "Index"


class VariedMethodsView(FlaskView):

    def index(self):
        return "Index"

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @classmethod
    def class_method(cls):
        return "Class Method"


class SubVariedMethodsView(VariedMethodsView):
    pass


def func_decorator(f):
    def decorated_view(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_view


def params_decorator(p_1, p_2):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def recursive_decorator(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        decorated_view.foo()
        return f(*args, **kwargs)

    def foo():
        return 'bar'
    decorated_view.foo = foo
    return decorated_view


def more_recursive(stop_type):
    def _inner(func):
        def _recursive(*args, **kw):
            return func(*args, **kw)
        return _recursive
    return _inner


class DecoratedView(FlaskView):
    @func_decorator
    def index(self):
        return "Index"

    @func_decorator
    def get(self, id):
        return "Get " + id

    @recursive_decorator
    def post(self):
        return "Post"

    @params_decorator("oneval", "anotherval")
    def params_decorator_method(self):
        return "Params Decorator"

    @params_decorator(get_value(), "value")
    def delete(self, obj_id):
        return "Params Decorator Delete " + obj_id

    @more_recursive(None)
    def get_some(self):
        return "Get Some"

    @more_recursive(None)
    @recursive_decorator
    def get_this(self):
        return "Get This"

    @route('/mixitup')
    @more_recursive(None)
    @recursive_decorator
    def mixitup(self):
        return "Mix It Up"

    @more_recursive(None)
    def someval(self, val):
        return "Someval " + val

    @route('/anotherval/<val>')
    @more_recursive(None)
    @recursive_decorator
    def anotherval(self, val):
        return "Anotherval " + val


class InheritanceView(BasicView):

    # Tests method override
    def get(self, obj_id):
        return "Inheritance Get " + obj_id

    @route('/<obj_id>/delete', methods=['DELETE'])
    def delete(self, obj_id):
        return "Inheritance Delete " + obj_id

    @route('/with_route')
    def with_route(self):
        return "Inheritance with route"


class DecoratedInheritanceView(DecoratedView):

    @recursive_decorator
    def get(self, obj_id):
        return "Decorated Inheritance Get " + obj_id


class TrailingSlashView(FlaskView):
    trailing_slash = False
    route_base = '/trailing/'

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id

    def put(self, id):
        return "Put " + id

    def patch(self, id):
        return "Patch " + id

    # def post(self):
    #     return "Post"

    @route('', methods=['POST'])
    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    def custom_method(self):
        return "Custom Method"

    def custom_method_with_params(self, p_one, p_two):
        return "Custom Method {0!s} {1!s}".format(p_one, p_two)

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @route("/routed2")
    def routed_method2(self):
        return "Routed Method 2"


class InheritedTrailingSlashView(TrailingSlashView):
    route_base = '/inherited/trailing/'

    def index(self):
        return "Index"


class OverrideInheritedTrailingSlashView(TrailingSlashView):
    route_base = "/override/trailing/"
    trailing_slash = True

    def index(self):
        return "Index"


class EnabledHasTrailingSlashView(FlaskView):
    route_base = '/enabled-trailing-yes/'

    def index(self):
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id


class EnabledNoTrailingSlashView(FlaskView):
    route_base = '/enabled-trailing-no'

    def index(self):
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id


class JSONifyTestView(FlaskView):
    route_base = '/jsonify'
    trailing_slash = False

    def index(self):
        return jsonify(dict(
            success=True
        )), 200

    def post(self):
        return jsonify(dict(
            success=True
        )), 201

    @route('/not-found', methods=['GET'])
    def not_found(self):
        return jsonify(dict(
            success=False
        )), 404

    @route('/custom-header', methods=['GET'])
    def custom_header(self):
        return jsonify(dict(
            success=True
        )), 418, {'X-TEAPOT': '1'}

    @route('/normal')
    def normal_jsonify(self):
        return jsonify(dict(
            success=True
        ))


def make_bold_decorator(fn):
    """Wraps a view function with Bold"""
    @wraps(fn)
    def inner(*args, **kwargs):
        return '<b>' + fn(*args, **kwargs) + '</b>'
    return inner


def make_italics_decorator(fn):
    """Wraps a view function with Italics"""
    @wraps(fn)
    def inner(*args, **kwargs):
        return '<i>' + fn(*args, **kwargs) + '</i>'
    return inner


def make_paragraph_decorator(fn):
    """Wraps a view function with Paragraph"""
    @wraps(fn)
    def inner(*args, **kwargs):
        return '<p>' + fn(*args, **kwargs) + '</p>'
    return inner


class DecoratedBoldListView(FlaskView):
    """View class that applies bold to every route"""
    route_base = '/decorated_bold_list_view/'
    decorators = [make_bold_decorator]

    def get(self, id):
        """Get an individual resource"""
        return 'Get {0!s}'.format(id)

    def index(self):
        """Get the index"""
        return 'Index'


class DecoratedBoldItalicsListView(FlaskView):
    """View class that applies bold and italics to every route"""
    route_base = '/decorated_bold_italics_list_view/'
    decorators = [make_bold_decorator, make_italics_decorator]

    def get(self, id):
        """Get an individual resource"""
        return 'Get {0!s}'.format(id)

    def index(self):
        """Get the index"""
        return 'Index'


class DecoratedListMemberView(FlaskView):
    """
    View class that decorators to every route and a decorator
    to an individual route
    """
    route_base = '/decorated_list_member_view/'
    decorators = [
        # Third Decorator
        make_bold_decorator,

        # Second Decorator
        make_italics_decorator
    ]

    # First decorator
    @make_paragraph_decorator
    def get(self, id):
        """Get an individual resource"""
        return 'Get {0!s}'.format(id)

    def index(self):
        """Get the index"""
        return 'Index'


def eggs_attribute_decorator(eggs_style):
    """Applies the eggs style attribute to the function"""
    def decorator(f):
        f.eggs = eggs_style

        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class DecoratedListFunctionAttributesView(FlaskView):
    """
    View class that applies an attribute to a function via a
    decorator in the decorator list
    """
    route_base = '/decorated_list_function_attributes_view/'
    decorators = [
        make_italics_decorator,
        eggs_attribute_decorator('scrambled')
    ]

    @make_bold_decorator
    def get(self, id):
        """Get an individual resource"""
        return 'Get {0!s}'.format(id)

    def index(self):
        """Get the index"""
        return 'Index'


class DecoratedListMemberFunctionAttributesView(FlaskView):
    """
    View class that applies an attribute to a function via a
    decorator on the member function
    """
    route_base = '/decorated_list_member_function_attributes_view/'
    decorators = [make_italics_decorator]

    @make_bold_decorator
    def get(self, id):
        """Get an individual resource"""
        return 'Get {0!s}'.format(id)

    @eggs_attribute_decorator('scrambled')
    def index(self):
        """Get the index"""
        return 'Index'


def append_test_class_attribute_decorator(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        test_cls_attribute = getattr(fn.class_, "test")
        return fn(*args, **kwargs) + test_cls_attribute
    return inner


class DecoratedAppendClassAttributeView(FlaskView):
    """
    View class that appends the value of the class attribute
    `test` to the response.
    """
    route_base = '/decorated_append_class_attribute_view/'
    decorators = [append_test_class_attribute_decorator]

    test = " (this is a test)"

    def index(self):
        """Get the index"""
        return "Index"

class InspectArgsView(FlaskView):

    def foo(self, arg1, arg2, kwarg1=678):
        return 'foo %s(%s) %s(%s) %s(%s)' % (
            type(arg1).__name__, arg1,
            type(arg2).__name__, arg2,
            type(kwarg1).__name__, kwarg1
        )

class InspectArgsFalseView(FlaskView):
    def foo():
        pass

def coerce(**kwargs):
    def wrap(fn):
        @wraps(fn)
        def wrapped(*args, **kw):
            params = request.args
            newkw = {}
            for k, func in kwargs.items():
                if not k in params:
                    continue
                v = params[k]
                newkw[k] = func(v)
            return fn(*args, **newkw)
        return wrapped
    return wrap


class NoInspectArgsView(FlaskView):
    inspect_args = False

    @coerce(arg1=int, arg2=int, kwarg1=int)
    def foo(self, arg1=1, arg2=2, kwarg1=678):
        return 'foo %s(%s) %s(%s) %s(%s)' % (
            type(arg1).__name__, arg1,
            type(arg2).__name__, arg2,
            type(kwarg1).__name__, kwarg1
        )


class DefaultMethodsView(FlaskView):
    default_methods= ['GET', 'POST']

    def foo(self):
        return request.method


class NoDefaultMethodsView(FlaskView):

    def foo(self):
        return request.method


class WithInitArgument(FlaskView):
    """
    View class that receives in the constructor a parameter
    """
    route_base = '/with_init_argument/'

    def __init__(self, init_argument):
        self._init_argument = init_argument

    def get(self):
        return jsonify({ "init_argument": self._init_argument }), 200


class WithoutInitArgument(FlaskView):
    """
    View class that does not receive in the constructor a parameter
    For checking backwards compatibility
    """
    route_base = '/without_init_argument/'

    def __init__(self):
        self._init_argument = "not sent"

    def get(self):
        return jsonify({ "init_argument": self._init_argument }), 200


class AsyncView(FlaskView):

    async def get(self):
        await asyncio.sleep(0)
        return 'GET'

    async def post(self):
        await asyncio.sleep(0)
        return 'POST'


class BeforeRequestAsyncView(FlaskView):

    async def before_request(self, name):
        await asyncio.sleep(0)
        self.response = "Before Request"

    def index(self):
        return self.response


class BeforeViewAsyncView(FlaskView):

    async def before_index(self):
        await asyncio.sleep(0)
        self.response = "Before View"

    def index(self):
        return self.response


class AfterViewAsyncView(FlaskView):

    async def after_index(self, response):
        await asyncio.sleep(0)
        return "After View"

    def index(self):
        return "Index"


class AfterRequestAsyncView(FlaskView):

    async def after_request(self, name, response):
        await asyncio.sleep(0)
        return "After Request"

    def index(self):
        return "Index"
