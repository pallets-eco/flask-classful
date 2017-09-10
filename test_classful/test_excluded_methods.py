from flask import Flask

from flask_classful import FlaskView
from nose.tools import eq_


class NormalMethodsView(FlaskView):

    def copy_form_data(self):
        return "copy form data"


class ExcludedMethodsView(FlaskView):

    excluded_methods = ["copy_form_data"]

    def copy_form_data(self):
        return "copy form data"


app = Flask(__name__)
NormalMethodsView.register(app)
ExcludedMethodsView.register(app)

client = app.test_client()


def test_normal_methods_copy_form_data():
    resp = client.get("/normal-methods/copy_form_data/")
    eq_(b"copy form data", resp.data)


def test_excluded_methods_copy_form_data():
    resp = client.get("/excluded-methods/copy_form_data/")
    eq_(resp.status_code, 404)
