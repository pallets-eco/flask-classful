from flask import Flask
from .view_classes import DefaultMethodsView, NoDefaultMethodsView

app = Flask('default_methods')

DefaultMethodsView.register(app)
NoDefaultMethodsView.register(app)


def test_default_methods():
    client = app.test_client()
    resp = client.get('/default-methods/foo/')
    assert b"GET" == resp.data
    resp = client.post('/default-methods/foo/')
    assert b"POST" == resp.data


def test_no_default_methods():
    client = app.test_client()
    resp = client.get('/no-default-methods/foo/')
    assert b"GET" == resp.data
    resp = client.post('/no-default-methods/foo/')
    assert resp.status_code == 405
