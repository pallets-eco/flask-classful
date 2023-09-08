from flask import Flask
from .view_classes import InheritanceView, DecoratedInheritanceView

app = Flask("inheritance")
InheritanceView.register(app)
DecoratedInheritanceView.register(app)

client = app.test_client()


def test_index():
    resp = client.get("/inheritance/")
    assert b"Index" == resp.data


def test_override():
    resp = client.get("/inheritance/1234/")
    assert b"Inheritance Get 1234" == resp.data
    resp = client.get("/inheritance/1234")
    assert resp.status_code == 308


def test_inherited():
    resp = client.post("/inheritance/")
    assert b"Post" == resp.data


def test_with_route():
    resp = client.get("/inheritance/with_route")
    assert b"Inheritance with route" == resp.data


def test_override_with_route():
    resp = client.delete("/inheritance/1234/delete")
    assert b"Inheritance Delete 1234" == resp.data


def test_inherited_base_route():
    resp = client.get("/inheritance/routed/")
    assert b"Routed Method" == resp.data


def test_decorated_inherited_mixitup():
    resp = client.get("/decorated-inheritance/mixitup/")
    assert b"Mix It Up" == resp.data


def test_decorated_inheritance_get():
    resp = client.get("/decorated-inheritance/1234/")
    assert b"Decorated Inheritance Get 1234" == resp.data
    resp = client.get("/decorated-inheritance/1234")
    assert resp.status_code == 308
