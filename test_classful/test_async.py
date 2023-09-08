import flask
from functools import wraps
from nose import SkipTest
from nose.tools import eq_
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
skip_test = int(flask.__version__[0]) < 2


def skip_conditionally(test):
    @wraps(test)
    def skip():
        if skip_test:
            raise SkipTest('Skipping async views tests for this Flask version...')
        test()
    return skip


@skip_conditionally
def test_async_view():
    resp = client.get('/async/')
    eq_(b"GET", resp.data)
    resp = client.post('/async/')
    eq_(b"POST", resp.data)


@skip_conditionally
def test_async_before_request():
    resp = client.get("/before-request-async/")
    eq_(b"Before Request", resp.data)


@skip_conditionally
def test_async_before_view():
    resp = client.get("/before-view-async/")
    eq_(b"Before View", resp.data)


@skip_conditionally
def test_async_after_view():
    resp = client.get("/after-view-async/")
    eq_(b"After View", resp.data)


@skip_conditionally
def test_async_after_request():
    resp = client.get("/after-request-async/")
    eq_(b"After Request", resp.data)
