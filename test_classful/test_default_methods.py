from flask import Flask
from .view_classes import DefaultMethodsView, NoDefaultMethodsView
from nose.tools import eq_

app = Flask('default_methods')

DefaultMethodsView.register(app)
NoDefaultMethodsView.register(app)


def test_default_methods():
    client = app.test_client()
    resp = client.get('/default-methods/foo/')
    eq_(b"GET", resp.data)
    resp = client.post('/default-methods/foo/')
    eq_(b"POST", resp.data)


def test_no_default_methods():
    client = app.test_client()
    resp = client.get('/no-default-methods/foo/')
    eq_(b"GET", resp.data)
    resp = client.post('/no-default-methods/foo/')
    eq_(resp.status_code, 405)
