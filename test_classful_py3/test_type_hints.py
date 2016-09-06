from uuid import UUID
from flask import Flask
from flask_classful import FlaskView, route
from nose.tools import *


# python3 only

class TypingView(FlaskView):

    def index(self):
        return "Index"

    @route('/<id>', methods=['POST'])
    def post(self, id: str) -> str:
        return "Post"

    def patch(self, id: str) -> str:
        return "Patch"

    def int(self, arg: int):
        return str(arg)

    def float(self, arg: float):
        return str(arg)

    def uuid(self, arg: UUID):
        return str(arg)

app = Flask('typing-app')
TypingView.register(app)
client = app.test_client()


def test_index():
    resp = client.get('/typing/')
    eq_(b"Index", resp.data)


def test_post():
    resp = client.post('/typing/123')
    eq_(b"Post", resp.data)


def test_patch():
    resp = client.patch('/typing/123')
    eq_(b"Patch", resp.data)


def test_url_converter():
    for type_, wrong_var, correct_var in [
        ('int', 'asdfsdf', '1'),
        ('float', 'sdfad', '1.1'),
        ('uuid', '10', '1f5018ba-1a86-4f7f-a6c5-596674562f36')
    ]:
        url = '/typing/{}/{}'
        resp = client.get(url.format(type_, wrong_var))
        # should not match the endpoint if url variable type mismatches
        eq_(resp.status_code, 404)
        resp = client.get(url.format(type_, correct_var))
        eq_(resp.status_code, 200)
        eq_(bytes(correct_var, 'utf-8'), resp.data)
