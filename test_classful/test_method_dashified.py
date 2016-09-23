from flask import Flask
from flask_classful import FlaskView
from nose.tools import eq_


class DashifiedDefaultView(FlaskView):

    def some_route(self):
        return "some route"


class DashifiedAttributeView(FlaskView):
    method_dashified = True

    def another_route(self):
        return "another route"


class DashifiedAttributeOverrideView(FlaskView):
    method_dashified = True

    def yet_another_route(self):
        return "yet another route"


app = Flask('test-app')
DashifiedDefaultView.register(app, method_dashified=True)
DashifiedAttributeView.register(app)
DashifiedAttributeOverrideView.register(app, method_dashified=False)
client = app.test_client()


def test_original_method_dashifield():
    eq_(False, DashifiedDefaultView.method_dashified)
    eq_(True, DashifiedAttributeView.method_dashified)
    eq_(True, DashifiedAttributeOverrideView.method_dashified)


def test_some_route():
    resp = client.get('/dashified-default/some-route/')
    eq_(b"some route", resp.data)


def test_another_route():
    resp = client.get('/dashified-attribute/another-route/')
    eq_(b"another route", resp.data)


def test_yet_another_route():
    resp = client.get('/dashified-attribute-override/yet_another_route/')
    eq_(b"yet another route", resp.data)
