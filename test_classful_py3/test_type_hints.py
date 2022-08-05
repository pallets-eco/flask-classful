from uuid import UUID
from flask import Flask
from flask_classful import FlaskView, route


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
    assert b"Index" == resp.data
    resp = client.get('/typing')
    assert resp.status_code == 308


def test_post():
    resp = client.post('/typing/123')
    assert b"Post" == resp.data
    resp = client.post('/typing/123/')
    assert resp.status_code == 405


def test_patch():
    resp = client.patch('/typing/123/')
    assert b"Patch" == resp.data
    resp = client.patch('/typing/123')
    assert resp.status_code == 308


def test_url_converter():
    for type_, wrong_var, correct_var in [
        ('int', 'asdfsdf', '1'),
        ('float', 'sdfad', '1.1'),
        ('uuid', '10', '1f5018ba-1a86-4f7f-a6c5-596674562f36')
    ]:
        url = '/typing/{}/{}/'
        resp = client.get(url.format(type_, wrong_var))
        # should not match the endpoint if url variable type mismatches
        assert resp.status_code == 404
        resp = client.get(url.format(type_, correct_var))
        assert resp.status_code == 200
        assert bytes(correct_var, 'utf-8') == resp.data
