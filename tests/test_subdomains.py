from flask import Flask

from .view_classes import BasicView

app = Flask("common")
app.config["SERVER_NAME"] = "test.test"
BasicView.register(app, subdomain="basic")

client = app.test_client()


def test_index_subdomain():
    resp = client.get("/basic/", base_url="http://basic.test.test")
    assert b"Index" == resp.data


def test_get():
    resp = client.get("/basic/1234/", base_url="http://basic.test.test")
    assert b"Get 1234" == resp.data
    resp = client.get("/basic/1234", base_url="http://basic.test.test")
    assert resp.status_code == 308


def test_put():
    resp = client.put("/basic/1234/", base_url="http://basic.test.test")
    assert b"Put 1234" == resp.data
    resp = client.put("/basic/1234", base_url="http://basic.test.test")
    assert resp.status_code == 308


def test_patch():
    resp = client.patch("/basic/1234/", base_url="http://basic.test.test")
    assert b"Patch 1234" == resp.data
    resp = client.patch("/basic/1234", base_url="http://basic.test.test")
    assert resp.status_code == 308


def test_post():
    resp = client.post("/basic/", base_url="http://basic.test.test")
    assert b"Post" == resp.data


def test_delete():
    resp = client.delete("/basic/1234/", base_url="http://basic.test.test")
    assert b"Delete 1234" == resp.data
    resp = client.delete("/basic/1234", base_url="http://basic.test.test")
    assert resp.status_code == 308


def test_custom_method():
    resp = client.get("/basic/custom_method/", base_url="http://basic.test.test")
    assert b"Custom Method" == resp.data


def test_custom_method_with_params():
    resp = client.get(
        "/basic/custom_method_with_params/1234/abcd/", base_url="http://basic.test.test"
    )
    assert b"Custom Method 1234 abcd" == resp.data
    resp = client.get(
        "/basic/custom_method_with_params/1234/abcd", base_url="http://basic.test.test"
    )
    assert resp.status_code == 308


def test_routed_method():
    resp = client.get("/basic/routed/", base_url="http://basic.test.test")
    assert b"Routed Method" == resp.data


def test_multi_routed_method():
    resp = client.get("/basic/route1/", base_url="http://basic.test.test")
    assert b"Multi Routed Method" == resp.data

    resp = client.get("/basic/route2/", base_url="http://basic.test.test")
    assert b"Multi Routed Method" == resp.data


def test_no_slash():
    resp = client.get("/basic/noslash", base_url="http://basic.test.test")
    assert b"No Slash Method" == resp.data
