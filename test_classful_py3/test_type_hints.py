import json
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
