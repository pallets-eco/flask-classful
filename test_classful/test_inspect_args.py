import sys
from flask import Flask
from .view_classes import InspectArgsView, NoInspectArgsView, InspectArgsFalseView
from flask_classful import DecoratorCompatibilityError
from pytest import raises


_py2 = sys.version_info[0] == 2

app = Flask('inspect_args')

InspectArgsView.register(app)
NoInspectArgsView.register(app)


def test_inspect_args():
    client = app.test_client()
    resp = client.get('/inspect-args/foo/123/456/')
    expected = b"foo str(123) str(456) int(678)"

    if _py2:
        expected = b"foo unicode(123) unicode(456) int(678)"
    assert expected == resp.data
    resp = client.get('/inspect-args/foo/123/456')
    assert resp.status_code == 308


def test_no_inspect_args():
    client = app.test_client()
    resp = client.get('/no-inspect-args/foo/', query_string={'arg1': 123, 'arg2': 456})
    assert b"foo int(123) int(456) int(678)" == resp.data


def test_inspect_args_error():
    with raises(DecoratorCompatibilityError):
        InspectArgsFalseView.register(app)

