from flask import Flask, request
from flask_classful import get_interesting_members, FlaskView
from nose.tools import eq_, raises

class BaseClass():
    def put(self):
        pass

class ChildClassView(FlaskView):
    def post(self):
        return request.method

    def put(self):
        return request.method


app = Flask('register')
ChildClassView.register(app, base_class=BaseClass)

@raises(TypeError)
def test_register_is_not_correct():
    FlaskView.register(app)

def test_child_class():
    """It can use method of child class normally"""
    client = app.test_client()
    resp = client.post('/child-class/')
    eq_(b"POST", resp.data)

def test_base_class():
    """It filter out the method has in base class"""
    client = app.test_client()
    resp = client.put('/child-class/')
    eq_(resp.status_code, 405)
