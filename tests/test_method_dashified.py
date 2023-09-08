from flask import Flask

from flask_classful import FlaskView


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


app = Flask("test-app")
DashifiedDefaultView.register(app, method_dashified=True)
DashifiedAttributeView.register(app)
DashifiedAttributeOverrideView.register(app, method_dashified=False)
client = app.test_client()


def test_original_method_dashifield():
    assert False is DashifiedDefaultView.method_dashified
    assert True is DashifiedAttributeView.method_dashified
    assert True is DashifiedAttributeOverrideView.method_dashified


def test_some_route():
    resp = client.get("/dashified-default/some-route/")
    assert b"some route" == resp.data


def test_another_route():
    resp = client.get("/dashified-attribute/another-route/")
    assert b"another route" == resp.data


def test_yet_another_route():
    resp = client.get("/dashified-attribute-override/yet_another_route/")
    assert b"yet another route" == resp.data
