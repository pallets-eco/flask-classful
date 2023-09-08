import flask
import pytest
from packaging import version
from .view_classes import (
    AsyncView,
    BeforeRequestAsyncView,
    BeforeViewAsyncView,
    AfterRequestAsyncView,
    AfterViewAsyncView
)

app = flask.Flask(__name__)
AsyncView.register(app)
BeforeRequestAsyncView.register(app)
BeforeViewAsyncView.register(app)
AfterViewAsyncView.register(app)
AfterRequestAsyncView.register(app)

client = app.test_client()
skip_test = version.parse(flask.__version__) < version.parse("2")
skip_reason = "Skipping async views tests for Flask<2..."


@pytest.mark.skipif(condition=skip_test, reason=skip_reason)
def test_async_view():
    resp = client.get('/async/')
    assert b"GET" == resp.data
    resp = client.post('/async/')
    assert b"POST" == resp.data


@pytest.mark.skipif(condition=skip_test, reason=skip_reason)
def test_async_before_request():
    resp = client.get("/before-request-async/")
    assert b"Before Request" == resp.data


@pytest.mark.skipif(condition=skip_test, reason=skip_reason)
def test_async_before_view():
    resp = client.get("/before-view-async/")
    assert b"Before View" == resp.data


@pytest.mark.skipif(condition=skip_test, reason=skip_reason)
def test_async_after_view():
    resp = client.get("/after-view-async/")
    assert b"After View" == resp.data


@pytest.mark.skipif(condition=skip_test, reason=skip_reason)
def test_async_after_request():
    resp = client.get("/after-request-async/")
    assert b"After Request" == resp.data
