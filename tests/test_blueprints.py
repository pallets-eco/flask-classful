import json

from flask import Blueprint
from flask import Flask

from .view_classes import BasicView
from .view_classes import IndexView
from .view_classes import JSONifyTestView

app = Flask("blueprints")
bp = Blueprint("bptest", "bptest")
BasicView.register(bp)
IndexView.register(bp)
JSONifyTestView.register(bp)
app.register_blueprint(bp)

client = app.test_client()


def test_bp_index():
    resp = client.get("/basic/")
    assert b"Index" == resp.data


def test_bp_get():
    resp = client.get("/basic/1234/")
    assert b"Get 1234" == resp.data
    resp = client.get("/basic/1234")
    print(resp)
    assert resp.status_code == 308


def test_bp_put():
    resp = client.put("/basic/1234/")
    assert b"Put 1234" == resp.data
    resp = client.put("/basic/1234")
    assert resp.status_code == 308


def test_bp_patch():
    resp = client.patch("/basic/1234/")
    assert b"Patch 1234" == resp.data
    resp = client.patch("/basic/1234")
    assert resp.status_code == 308


def test_bp_post():
    resp = client.post("/basic/")
    assert b"Post" == resp.data


def test_bp_delete():
    resp = client.delete("/basic/1234/")
    assert b"Delete 1234" == resp.data
    resp = client.delete("/basic/1234")
    assert resp.status_code == 308


def test_bp_custom_method():
    resp = client.get("/basic/custom_method/")
    assert b"Custom Method" == resp.data
    resp = client.get("/basic/custom_method")
    assert resp.status_code == 308


def test_bp_custom_method_with_params():
    resp = client.get("/basic/custom_method_with_params/1234/abcd/")
    assert b"Custom Method 1234 abcd" == resp.data
    resp = client.get("/basic/custom_method_with_params/1234/abcd")
    assert resp.status_code == 308


def test_bp_routed_method():
    resp = client.get("/basic/routed/")
    assert b"Routed Method" == resp.data


def test_bp_multi_routed_method():
    resp = client.get("/basic/route1/")
    assert b"Multi Routed Method" == resp.data

    resp = client.get("/basic/route2/")
    assert b"Multi Routed Method" == resp.data


def test_bp_no_slash():
    resp = client.get("/basic/noslash")
    assert b"No Slash Method" == resp.data
    resp = client.get("/basic/noslash/")  # matches get(id)
    assert b"Get noslash" == resp.data


def test_bp_index_view_index():
    resp = client.get("/")
    assert b"Index" == resp.data


def test_bp_custom_http_method():
    resp = client.post("/basic/route3/")
    assert b"Custom HTTP Method" == resp.data


def test_bp_url_prefix():
    app = Flask("blueprints")
    foo = Blueprint("foo", __name__)
    BasicView.register(foo, route_base="/")
    app.register_blueprint(foo, url_prefix="/foo")

    client = app.test_client()
    resp = client.get("/foo/")
    assert b"Index" == resp.data


def test_jsonify_normal_index():
    resp = client.get("/jsonify")
    assert resp.status_code == 200
    assert json.loads(resp.data.decode("utf-8")) == dict(success=True)


def test_jsonify_post_custom_status_code():
    resp = client.post("/jsonify")
    assert resp.status_code == 201
    assert json.loads(resp.data.decode("utf-8")) == dict(success=True)


def test_jsonify_not_found():
    resp = client.get("/jsonify/not-found")
    assert resp.status_code == 404
    assert json.loads(resp.data.decode("utf-8")) == dict(success=False)


def test_custom_header():
    resp = client.get("/jsonify/custom-header")
    assert resp.status_code == 418
    assert resp.headers["X-TEAPOT"] == "1"
    assert json.loads(resp.data.decode("utf-8")) == dict(success=True)


def test_normal_jsonify():
    resp = client.get("/jsonify/normal")
    assert resp.status_code == 200
    assert resp.headers is not None
    assert json.loads(resp.data.decode("utf-8")) == dict(success=True)
