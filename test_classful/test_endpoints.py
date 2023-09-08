from flask import Flask, url_for
from .view_classes import BasicView, IndexView, RouteBaseView, VarBaseView

app = Flask("common")
BasicView.register(app)
IndexView.register(app)
RouteBaseView.register(app)
VarBaseView.register(app)

client = app.test_client()


def test_index_url():
    with app.test_request_context():
        url = url_for("IndexView:index")
        assert "/" == url


def test_basic_index_url():
    with app.test_request_context():
        url = url_for("BasicView:index")
        assert "/basic/" == url


def test_custom_endpoint_url():
    with app.test_request_context():
        url = url_for("basic_endpoint")
        assert "/basic/endpoint/" == url


def test_custom_route_base():
    with app.test_request_context():
        url = url_for('RouteBaseView:index')
        assert "/base-routed/" == url


def test_variable_route_popped_base():
    with app.test_request_context():
        url = url_for('VarBaseView:index', route='bar')
        assert '/var-base-route/bar/' == url


def test_variable_route_base():
    with app.test_request_context():
        url = url_for('VarBaseView:with_base_arg', route='bar')
        assert '/var-base-route/bar/with_base_arg/' == url


def test_variable_route_base_with_local_route_var():
    client = app.test_client()
    resp = client.get('/var-base-route/bar/local/baz')
    assert resp.data == b"bar baz"
