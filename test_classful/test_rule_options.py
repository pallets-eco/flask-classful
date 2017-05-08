from .view_classes import BasicView, IndexView
from flask import Flask
from nose.tools import eq_

app = Flask("rules_options")
BasicView.register(app, strict_slashes=False)
IndexView.register(app, strict_slashes=False)

client = app.test_client()

def test_rule_options_index():
    resp = client.get("/basic/")
    eq_(b"Index", resp.data)

    resp = client.get("/basic")
    eq_(b"Index", resp.data)


def test_rule_options_get():
    resp = client.get("/basic/1234/")
    eq_(resp.status_code, 404)
    eq_(b"Get 1234", resp.data)

    resp = client.get("/basic/1234")
    eq_(resp.status_code, 404)
    eq_(b"Get 1234", resp.data)


def test_rule_options_put():
    resp = client.put("/basic/1234/")
    eq_(resp.status_code, 403)
    eq_(resp.headers['say'], 'hello')
    eq_(b"Put 1234", resp.data)

    resp = client.put("/basic/1234")
    eq_(resp.status_code, 403)
    eq_(resp.headers['say'], 'hello')
    eq_(b"Put 1234", resp.data)


def test_rule_options_patch():
    resp = client.patch("/basic/1234/")
    eq_(b"Patch 1234", resp.data)

    resp = client.patch("/basic/1234")
    eq_(b"Patch 1234", resp.data)


def test_rule_options_post():
    resp = client.post("/basic/")
    eq_(b"Post", resp.data)

    resp = client.post("/basic")
    eq_(b"Post", resp.data)


def test_rule_options_delete():
    resp = client.delete("/basic/1234/")
    eq_(b"Delete 1234", resp.data)

    resp = client.delete("/basic/1234")
    eq_(b"Delete 1234", resp.data)

def test_rule_options_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_(b"Custom Method", resp.data)

    resp = client.get("/basic/custom_method")
    eq_(b"Custom Method", resp.data)


def test_rule_options_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    eq_(b"Custom Method 1234 abcd", resp.data)

    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_(b"Custom Method 1234 abcd", resp.data)

