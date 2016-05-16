import json

from flask import Flask, Blueprint
from .view_classes import BasicView, IndexView, JSONifyTestView
from nose.tools import *

app = Flask("blueprints")
bp = Blueprint("bptest", "bptest")
BasicView.register(bp)
IndexView.register(bp)
JSONifyTestView.register(bp)
app.register_blueprint(bp)

client = app.test_client()

def test_bp_index():
    resp = client.get("/basic/")
    eq_(b"Index", resp.data)

def test_bp_get():
    resp = client.get("/basic/1234")
    eq_(b"Get 1234", resp.data)

def test_bp_put():
    resp = client.put("/basic/1234")
    eq_(b"Put 1234", resp.data)

def test_bp_patch():
    resp = client.patch("/basic/1234")
    eq_(b"Patch 1234", resp.data)

def test_bp_post():
    resp = client.post("/basic/")
    eq_(b"Post", resp.data)

def test_bp_delete():
    resp = client.delete("/basic/1234")
    eq_(b"Delete 1234", resp.data)

def test_bp_custom_method():
    resp = client.get("/basic/custom_method/")
    eq_(b"Custom Method", resp.data)

def test_bp_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    eq_(b"Custom Method 1234 abcd", resp.data)

def test_bp_routed_method():
    resp = client.get("/basic/routed/")
    eq_(b"Routed Method", resp.data)

def test_bp_multi_routed_method():
    resp = client.get("/basic/route1/")
    eq_(b"Multi Routed Method", resp.data)

    resp = client.get("/basic/route2/")
    eq_(b"Multi Routed Method", resp.data)

def test_bp_no_slash():
    resp = client.get("/basic/noslash")
    eq_(b"No Slash Method", resp.data)

def test_bp_index_view_index():
    resp = client.get("/")
    eq_(b"Index", resp.data)

def test_bp_custom_http_method():
    resp = client.post("/basic/route3/")
    eq_(b"Custom HTTP Method", resp.data)

def test_bp_url_prefix():
    foo = Blueprint('foo', __name__)
    BasicView.register(foo, route_base="/")
    app.register_blueprint(foo, url_prefix='/foo')

    resp = client.get('/foo/')
    eq_(b"Index", resp.data)


def test_jsonify_normal_index():
    resp = client.get('/jsonify')
    eq_(resp.status_code, 200)
    eq_(json.loads(resp.data.decode('utf-8')), dict(success=True))


def test_jsonify_post_custom_status_code():
    resp = client.post('/jsonify')
    eq_(resp.status_code, 201)
    eq_(json.loads(resp.data.decode('utf-8')), dict(success=True))


def test_jsonify_not_found():
    resp = client.get('/jsonify/not-found')
    eq_(resp.status_code, 404)
    eq_(json.loads(resp.data.decode('utf-8')), dict(success=False))


def test_custom_header():
    resp = client.get('/jsonify/custom-header')
    eq_(resp.status_code, 418)
    eq_(resp.headers['X-TEAPOT'], '1')
    eq_(json.loads(resp.data.decode('utf-8')), dict(success=True))


def test_normal_jsonify():
    resp = client.get('/jsonify/normal')
    eq_(resp.status_code, 200)
    eq_(resp.headers is not None, True)
    eq_(json.loads(resp.data.decode('utf-8')), dict(success=True))
