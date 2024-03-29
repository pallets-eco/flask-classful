import flask

from .view_classes import AfterRequestAsyncView
from .view_classes import AfterViewAsyncView
from .view_classes import AsyncView
from .view_classes import BeforeRequestAsyncView
from .view_classes import BeforeViewAsyncView

app = flask.Flask(__name__)
AsyncView.register(app)
BeforeRequestAsyncView.register(app)
BeforeViewAsyncView.register(app)
AfterViewAsyncView.register(app)
AfterRequestAsyncView.register(app)

client = app.test_client()


def test_async_view():
    resp = client.get("/async/")
    assert b"GET" == resp.data
    resp = client.post("/async/")
    assert b"POST" == resp.data


def test_async_before_request():
    resp = client.get("/before-request-async/")
    assert b"Before Request" == resp.data


def test_async_before_view():
    resp = client.get("/before-view-async/")
    assert b"Before View" == resp.data


def test_async_after_view():
    resp = client.get("/after-view-async/")
    assert b"After View" == resp.data


def test_async_after_request():
    resp = client.get("/after-request-async/")
    assert b"After Request" == resp.data
