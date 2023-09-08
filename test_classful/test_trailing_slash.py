from flask import Flask
from .view_classes import (
    BasicView,
    TrailingSlashView,
    InheritedTrailingSlashView,
    OverrideInheritedTrailingSlashView,
    EnabledHasTrailingSlashView,
    EnabledNoTrailingSlashView,
    IndexView
)

app = Flask('trailing_slash')
BasicView.register(app, trailing_slash=False)
TrailingSlashView.register(app)
InheritedTrailingSlashView.register(app)
OverrideInheritedTrailingSlashView.register(app)
EnabledHasTrailingSlashView.register(app)
EnabledNoTrailingSlashView.register(app)
IndexView.register(app, trailing_slash=False)

client = app.test_client()


def test_index():
    resp = client.get("/basic")
    assert b"Index" == resp.data
    resp = client.get("/basic/")
    assert resp.status_code == 404


def test_get():
    resp = client.get("/basic/1234")
    assert b"Get 1234" == resp.data
    resp = client.get("/basic/1234/")
    assert resp.status_code == 404


def test_put():
    resp = client.put("/basic/1234")
    assert b"Put 1234" == resp.data
    resp = client.put("/basic/1234/")
    assert resp.status_code == 404

def test_patch():
    resp = client.patch("/basic/1234")
    assert b"Patch 1234" == resp.data
    resp = client.patch("/basic/1234/")
    assert resp.status_code == 404


def test_post():
    resp = client.post("/basic")
    assert b"Post" == resp.data
    resp = client.post("/basic/")
    assert resp.status_code == 404


def test_delete():
    resp = client.delete("/basic/1234")
    assert b"Delete 1234" == resp.data
    resp = client.delete("/basic/1234/")
    assert resp.status_code == 404


def test_custom_method():
    resp = client.get("/basic/custom_method")
    assert b"Custom Method" == resp.data
    resp = client.get("/basic/custom_method/")
    assert resp.status_code == 404


def test_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    assert b"Custom Method 1234 abcd" == resp.data
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    assert resp.status_code == 404


def test_routed_method():
    resp = client.get("/basic/routed/")
    assert b"Routed Method" == resp.data
    resp = client.get("/basic/routed")
    assert resp.status_code == 308

# TrailingSlashView
def test_trailing_index():
    resp = client.get("/trailing")
    assert b"Index" == resp.data
    resp = client.get("/trailing/")
    assert resp.status_code == 404


def test_trailing_get():
    resp = client.get("/trailing/1234")
    assert b"Get 1234" == resp.data
    resp = client.get("/trailing/1234/")
    assert resp.status_code == 404


def test_trailing_put():
    resp = client.put("/trailing/1234")
    assert b"Put 1234" == resp.data
    resp = client.put("/trailing/1234/")
    assert resp.status_code == 404


def test_trailing_patch():
    resp = client.patch("/trailing/1234")
    assert b"Patch 1234" == resp.data
    resp = client.patch("/trailing/1234/")
    assert resp.status_code == 404


def test_trailing_post():
    resp = client.post("/trailing")
    assert b"Post" == resp.data
    resp = client.post("/trailing/")
    assert resp.status_code == 404

def test_trailing_delete():
    resp = client.delete("/trailing/1234")
    assert b"Delete 1234" == resp.data
    resp = client.delete("/trailing/1234/")
    assert resp.status_code == 404


def test_trailing_custom_method():
    resp = client.get("/trailing/custom_method")
    assert b"Custom Method" == resp.data
    resp = client.get("/trailing/custom_method/")
    assert resp.status_code == 404


def test_trailing_custom_method_with_params():
    resp = client.get("/trailing/custom_method_with_params/1234/abcd")
    assert b"Custom Method 1234 abcd" == resp.data
    resp = client.get("/trailing/custom_method_with_params/1234/abcd/")
    assert resp.status_code == 404


def test_trailing_routed_method():
    resp = client.get("/trailing/routed/")
    assert b"Routed Method" == resp.data
    resp = client.get("/trailing/routed")
    assert resp.status_code == 308


def test_trailing_routed_method2():
    resp = client.get("/trailing/routed2")
    assert b"Routed Method 2" == resp.data
    resp = client.get("/trailing/routed2/")
    assert resp.status_code == 404


# InheritedTrailingSlashView
def test_inherited_trailing_slash():
    resp = client.get("/inherited/trailing")
    assert b"Index" == resp.data
    resp = client.get("/inherited/trailing/")
    assert resp.status_code == 404


# OverrideInheritedTrailingSlashView
def test_inherited_trailing_slash_override():
    resp = client.get("/override/trailing/")
    assert b"Index" == resp.data
    resp = client.get("/override/trailing")
    assert resp.status_code == 308


# EnabledHasTrailingSlashView
def test_enabled_has_trailing_slash_view_index():
    resp = client.get("/enabled-trailing-yes/")
    assert b"Index" == resp.data
    resp = client.get("/enabled-trailing-yes")
    assert resp.status_code == 308


def test_enabled_has_trailing_slash_view_get():
    resp = client.get("/enabled-trailing-yes/1234/")
    assert b"Get 1234" == resp.data
    resp = client.get("/enabled-trailing-yes/1234")
    assert resp.status_code == 308


# EnabledNoTrailingSlashView
def test_enabled_no_trailing_slash_view_index():
    resp = client.get("/enabled-trailing-no/")
    assert b"Index" == resp.data
    resp = client.get("/enabled-trailing-no")
    assert resp.status_code == 308


def test_enabled_no_trailing_slash_view_get():
    resp = client.get("/enabled-trailing-no/1234/")
    assert b"Get 1234" == resp.data
    resp = client.get("/enabled-trailing-no/1234")
    assert resp.status_code == 308


# IndexView route_base '/' and trailing slash False
def test_index_trailing_slash():
    resp = client.get("/")
    assert b"Index" == resp.data
    resp = client.get("")
    assert resp.status_code == 308
