from flask import Flask
from flask_classful import unpack, get_true_argspec, method, route, DecoratorCompatibilityError
from .view_classes import BasicView, IndexView
from nose.tools import eq_, raises

app = Flask("common")
BasicView.register(app)
IndexView.register(app)

client = app.test_client()


def test_index():
    resp = client.get("/basic/")
    eq_(b"Index", resp.data)


def test_get():
    resp = client.get("/basic/1234/")
    eq_(resp.status_code, 404)
    eq_(b"Get 1234", resp.data)
    resp = client.get("/basic/1234")
    eq_(resp.status_code, 308)


def test_put():
    resp = client.put("/basic/1234/")
    eq_(resp.status_code, 403)
    eq_(resp.headers['say'], 'hello')
    eq_(b"Put 1234", resp.data)
    resp = client.put("/basic/1234")
    eq_(resp.status_code, 308)


def test_patch():
    resp = client.patch("/basic/1234/")
    eq_(b"Patch 1234", resp.data)
    resp = client.patch("/basic/1234")
    eq_(resp.status_code, 308)


def test_post():
    resp = client.post("/basic/")
    eq_(b"Post", resp.data)
    resp = client.post("/basic")
    eq_(resp.status_code, 308)


def test_delete():
    resp = client.delete("/basic/1234/")
    eq_(b"Delete 1234", resp.data)
    resp = client.delete("/basic/1234")
    eq_(resp.status_code, 308)


def test_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_(b"Custom Method", resp.data)
    resp = client.get("/basic/custom_method")
    eq_(resp.status_code, 308)


def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    eq_(b"Custom Method 1234 abcd", resp.data)
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_(resp.status_code, 308)


def test_routed_method():
    resp = client.get("/basic/routed/")
    eq_(b"Routed Method", resp.data)
    resp = client.get("/basic/routed")
    eq_(resp.status_code, 308)


def test_multi_routed_method():
    resp = client.get("/basic/route1/")
    eq_(b"Multi Routed Method", resp.data)
    resp = client.get("/basic/route1")
    eq_(resp.status_code, 308)

    resp = client.get("/basic/route2/")
    eq_(b"Multi Routed Method", resp.data)
    resp = client.get("/basic/route2")
    eq_(resp.status_code, 308)


def test_no_slash():
    resp = client.get("/basic/noslash")
    eq_(b"No Slash Method", resp.data)
    resp = client.get("/basic/noslash/") # matches get(id)
    eq_(b"Get noslash", resp.data)


def test_index_view_index():
    resp = client.get("/")
    eq_(b"Index", resp.data)
    resp = client.get("")
    eq_(resp.status_code, 308)


def test_custom_http_method():
    resp = client.post("/basic/route3/")
    eq_(b"Custom HTTP Method", resp.data)
    resp = client.post("/basic/route3")
    eq_(resp.status_code, 308)

def test_method_decorator_simple():
    resp = client.post("/basic/methoddecorated/")
    eq_(b"POST", resp.data)
    resp = client.post("/basic/methoddecorated")
    eq_(resp.status_code, 308)

def test_method_decorator_twice():
    resp = client.post('/basic/methodtwicedecorated/')
    eq_(b"POST", resp.data)
    resp = client.patch('/basic/methodtwicedecorated/')
    eq_(b"PATCH", resp.data)

def test_method_route():
   """Test that the @method decorator does not come into play when a route
   is set explicitly"""
   resp = client.post('/basic/methodroute')
   eq_(resp.status_code, 405)
   resp = client.get('/basic/methodroute')
   eq_(b"GET", resp.data)

def test_docstrings():
    proxy_func = app.view_functions["BasicView:index"]
    eq_(proxy_func.__doc__, BasicView.index.__doc__)

def test_unpack_tuple():
    """Test unpack tuple data"""
    response, code, headers = unpack(("response", 100, "c"))

    eq_("response", response)
    eq_(100, code)
    eq_("c", headers)

    response, code, headers = unpack(('response', 404))
    eq_("response", response)
    eq_(404, code)
    eq_({}, headers)

    response, code, headers = unpack(('response'))
    eq_("response", response)
    eq_(200, code)
    eq_({}, headers)

def test_unpack_not_tuple():
    """Test unpack not tuple data"""
    response, code, headers = unpack(None)

    eq_(None, response)
    eq_(200, code)
    eq_({}, headers)

    response, code, headers = unpack({})
    eq_({}, response)
    eq_(200, code)
    eq_({}, headers)

    response, code, headers = unpack("string")
    eq_("string", response)
    eq_(200, code)
    eq_({}, headers)

    response, code, headers = unpack(('response', 1, 2, 3, 4, 5))

    eq_(('response', 1, 2, 3, 4, 5), response)
    eq_(200, code)
    eq_({}, headers)

@raises(TypeError)
def test_get_true_argspec_raise_error():
    """Test get_true_argspec will raise error if method is not correct"""
    get_true_argspec(None)


def test_get_true_argspec_func():
    """Test get_true_argspec will use __func__ attr"""

    def _method():
        pass

    def _func(x):
        def _inner():
            return x
        return _inner

    setattr(_method, '__func__', _func(None))

    response = get_true_argspec(_method)

    eq_(None, response)

