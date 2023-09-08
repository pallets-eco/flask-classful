from flask import Flask

from .view_classes import AfterRequestView
from .view_classes import AfterViewView
from .view_classes import BeforeRequestReturnsView
from .view_classes import BeforeRequestView
from .view_classes import BeforeViewReturnsView
from .view_classes import BeforeViewView
from .view_classes import DecoratedView

app = Flask("wrappers")
BeforeRequestView.register(app)
BeforeRequestReturnsView.register(app)
BeforeViewView.register(app)
BeforeViewReturnsView.register(app)
AfterViewView.register(app)
AfterRequestView.register(app)
DecoratedView.register(app)

client = app.test_client()


def test_before_request():
    resp = client.get("/before-request/")
    assert b"Before Request" == resp.data


def test_before_view():
    resp = client.get("/before-view/")
    assert b"Before View" == resp.data


def test_after_view():
    resp = client.get("/after-view/")
    assert b"After View" == resp.data


def test_after_request():
    resp = client.get("/after-request/")
    assert b"After Request" == resp.data


def test_decorated_view():
    resp = client.get("/decorated/")
    assert b"Index" == resp.data

    resp = client.get("/decorated/1234/")
    assert b"Get 1234" == resp.data

    resp = client.get("/decorated/1234")
    assert resp.status_code == 308


def test_before_request_returns():
    resp = client.get("/before-request-returns/")
    assert b"BEFORE" == resp.data


def test_before_view_returns():
    resp = client.get("/before-view-returns/")
    assert b"BEFORE" == resp.data
