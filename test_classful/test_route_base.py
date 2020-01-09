from flask import Flask
from .view_classes import RouteBaseView, RouteBaseViewIsNotLatest
from nose.tools import eq_

app = Flask('route_base')
RouteBaseView.register(app, route_base="/rb_test2/")
RouteBaseViewIsNotLatest.register(app)


def test_route_base_override():
    client = app.test_client()
    resp = client.get('/rb_test2/')
    eq_(b"Index", resp.data)

def test_route_base_no_view():
    """Use class name as route"""
    client = app.test_client()
    resp = client.get('/route-base-view-is-not-latest/')
    eq_(b"Index", resp.data)
