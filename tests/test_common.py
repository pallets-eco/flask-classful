from flask import Flask
from flask_classful import unpack, get_true_argspec, method, route, DecoratorCompatibilityError
from .view_classes import BasicView, IndexView
from pytest import raises


app = Flask("common")
BasicView.register(app)
IndexView.register(app)


client = app.test_client()


def test_index():
    resp = client.get("/basic/")
    assert b"Index" == resp.data


def test_get():
    resp = client.get("/basic/1234/")
    assert resp.status_code == 404
    assert b"Get 1234" == resp.data
    resp = client.get("/basic/1234")
    assert resp.status_code == 308


def test_put():
    resp = client.put("/basic/1234/")
    assert resp.status_code == 403
    assert resp.headers['say'] == 'hello'
    assert b"Put 1234" == resp.data
    resp = client.put("/basic/1234")
    assert resp.status_code == 308


def test_patch():
    resp = client.patch("/basic/1234/")
    assert b"Patch 1234" == resp.data
    resp = client.patch("/basic/1234")
    assert resp.status_code == 308


def test_post():
    resp = client.post("/basic/")
    assert b"Post" == resp.data
    resp = client.post("/basic")
    assert resp.status_code == 308


def test_delete():
    resp = client.delete("/basic/1234/")
    assert b"Delete 1234" == resp.data
    resp = client.delete("/basic/1234")
    assert resp.status_code == 308


def test_custom_method():
    resp = client.get("/basic/custom_method/")
    assert b"Custom Method" == resp.data
    resp = client.get("/basic/custom_method")
    assert resp.status_code == 308


def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    assert b"Custom Method 1234 abcd" == resp.data
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    assert resp.status_code == 308


def test_routed_method():
    resp = client.get("/basic/routed/")
    assert b"Routed Method" == resp.data
    resp = client.get("/basic/routed")
    assert resp.status_code == 308


def test_multi_routed_method():
    resp = client.get("/basic/route1/")
    assert b"Multi Routed Method" == resp.data
    resp = client.get("/basic/route1")
    assert resp.status_code == 308

    resp = client.get("/basic/route2/")
    assert b"Multi Routed Method" == resp.data
    resp = client.get("/basic/route2")
    assert resp.status_code == 308


def test_no_slash():
    resp = client.get("/basic/noslash")
    assert b"No Slash Method" == resp.data
    resp = client.get("/basic/noslash/") # matches get(id)
    assert b"Get noslash" == resp.data


def test_index_view_index():
    resp = client.get("/")
    assert b"Index" == resp.data
    resp = client.get("")
    assert resp.status_code == 308


def test_custom_http_method():
    resp = client.post("/basic/route3/")
    assert b"Custom HTTP Method" == resp.data
    resp = client.post("/basic/route3")
    assert resp.status_code == 308

def test_method_decorator_simple():
    resp = client.post("/basic/methoddecorated/")
    assert b"POST" == resp.data
    resp = client.post("/basic/methoddecorated")
    assert resp.status_code == 308

def test_method_decorator_twice():
    resp = client.post('/basic/methodtwicedecorated/')
    assert b"POST" == resp.data
    resp = client.patch('/basic/methodtwicedecorated/')
    assert b"PATCH" == resp.data

def test_method_route():
   """Test that the @method decorator does not come into play when a route
   is set explicitly"""
   resp = client.post('/basic/methodroute')
   assert resp.status_code == 405
   resp = client.get('/basic/methodroute')
   assert b"GET" == resp.data

def test_docstrings():
    proxy_func = app.view_functions["BasicView:index"]
    assert proxy_func.__doc__ == BasicView.index.__doc__

def test_unpack_tuple():
    """Test unpack tuple data"""
    response, code, headers = unpack(("response", 100, "c"))

    assert "response" == response
    assert 100 == code
    assert "c" == headers

    response, code, headers = unpack(('response', 404))
    assert "response" == response
    assert 404 == code
    assert {} == headers

    response, code, headers = unpack(('response'))
    assert "response" == response
    assert 200 == code
    assert {} == headers

def test_unpack_not_tuple():
    """Test unpack not tuple data"""
    response, code, headers = unpack(None)

    assert None == response
    assert 200 == code
    assert {} == headers

    response, code, headers = unpack({})
    assert {} == response
    assert 200 == code
    assert {} == headers

    response, code, headers = unpack("string")
    assert "string" == response
    assert 200 == code
    assert {} == headers

    response, code, headers = unpack(('response', 1, 2, 3, 4, 5))

    assert ('response', 1, 2, 3, 4, 5) == response
    assert 200 == code
    assert {} == headers

def test_get_true_argspec_raise_error():
    """Test get_true_argspec will raise error if method is not correct"""
    with raises(TypeError):
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

    assert None == response

