import sys
from flask import Flask
from .view_classes import InspectArgsView, NoInspectArgsView, InspectArgsFalseView
from nose.tools import eq_, raises
from flask_classful import DecoratorCompatibilityError

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
    eq_(expected, resp.data)
    resp = client.get('/inspect-args/foo/123/456')
    eq_(resp.status_code, 308)


def test_no_inspect_args():
    client = app.test_client()
    resp = client.get('/no-inspect-args/foo/', query_string={'arg1': 123, 'arg2': 456})
    eq_(b"foo int(123) int(456) int(678)", resp.data)


@raises(DecoratorCompatibilityError)
def test_inspect_args_error():
    InspectArgsFalseView.register(app)

