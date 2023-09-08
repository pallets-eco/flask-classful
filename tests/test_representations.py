import json

from flask import Flask
from flask import make_response
from flask import redirect
from flask import request

from flask_classful import FlaskView


def output_json(data, code, headers=None):
    content_type = "application/json"
    dumped = json.dumps(data)
    if headers:
        headers.update({"Content-Type": content_type})
    else:
        headers = {"Content-Type": content_type}
    response = make_response(dumped, code, headers)
    return response


def output_default(data, code, headers=None):
    dumped = json.dumps(data)

    if headers:
        headers.update({"Content-Type": "flask-classful/default"})
    else:
        headers = {"Content-Type": "flask-classful/default"}
    response = make_response(dumped, code, headers)
    return response


# Test Responses
response_1 = {
    "internal_string": "just a string",
    "integer": 5,
    "validate_int": 1,
    "input_required": "just another string",
}
response_2 = {
    "internal_string": "What is going on",
    "integer": 3,
    "validate_int": 1,
    "input_required": "Nothing",
}
response_get = {
    "internal_string": "What is going on",
    "integer": 3,
    "validate_int": 1,
    "input_required": "GET",
}
response_put = {
    "internal_string": "What is going on",
    "integer": 3,
    "validate_int": 1,
    "input_required": "PUT",
}
response_post = {
    "internal_string": "What is going on",
    "integer": 3,
    "validate_int": 1,
    "input_required": "POST",
}
response_delete = {
    "internal_string": "What is going on",
    "integer": 3,
    "validate_int": 1,
    "input_required": "DELETE",
}

input_headers = [("Content-Type", "application/json"), ("Accept", "application/json")]
input_data = {"input_required": "required"}


class RepresentationView(FlaskView):
    representations = {"application/json": output_json}
    base_args = ["fields"]

    def index(self):
        return [response_1, response_2]

    def get(self, obj_id):
        return response_get

    def put(self, obj_id):
        return response_put, 403

    def post(self):
        return response_post, 404, {"say": "hello"}

    def delete(self, obj_id):
        return response_delete

    def mirror(self):
        out = request.args.get("q", "placeholder")

        return out, 201, {"Content-Type": "foo/bar"}

    def redirect(self):
        return redirect("http://google.com")


class DefaultRepresentationView(FlaskView):
    representations = {
        "application/json": output_json,
        "flask-classful/default": output_default,
    }

    def post(self):
        return request.get_json(), 201, {"say": "hello"}


app = Flask("representations")
RepresentationView.register(app)
DefaultRepresentationView.register(app, route_base="default")

client = app.test_client()


def test_index_representation():
    resp = client.get("/representation/", headers=input_headers)
    assert json.dumps([response_1, response_2]) == resp.data.decode("ascii")


def test_get_representation():
    resp = client.get("/representation/1/", headers=input_headers)
    assert json.dumps(response_get) == resp.data.decode("ascii")
    resp = client.get("/representation/1")
    assert resp.status_code == 308


def test_post_representation():
    resp = client.post(
        "/representation/", headers=input_headers, data=json.dumps(input_data)
    )
    assert resp.status_code, 404 == "should return 404 status code"
    assert resp.headers["say"] == "hello"
    assert json.dumps(response_post) == resp.data.decode("ascii")


def test_put_representation():
    resp = client.put(
        "/representation/1/", headers=input_headers, data=json.dumps(input_data)
    )
    assert resp.status_code, 403 == "should return 403 status code"
    assert json.dumps(response_put) == resp.data.decode("ascii")
    resp = client.put(
        "/representation/1", headers=input_headers, data=json.dumps(input_data)
    )
    assert resp.status_code == 308


def test_delete_representation():
    resp = client.delete("/representation/1/", headers=input_headers)
    assert json.dumps(response_delete) == resp.data.decode("ascii")
    resp = client.delete("/representation/1")
    assert resp.status_code == 308


def test_skip_representation_matching_if_response_is_returned():
    resp = client.get("/representation/redirect/")
    assert resp.status_code == 302
    assert resp.location == "http://google.com"


def test_representations_no_match_return_string():
    """If no matching Accept is found, Classful uses what view returns."""
    resp = client.get(
        "/representation/mirror/",
        query_string={"q": "foobar"},
        headers={"Accept": "foo/bar"},
    )

    assert resp.data == b"foobar"
    assert resp.headers["Content-Type"] == "foo/bar"
    assert resp.status_code == 201


def test_default_representation():
    """If a default representation is found, use it for no better match."""
    resp = client.post(
        "/default/",
        data=json.dumps({"foo": "bar"}),
        headers={"Accept": "foo/bar", "Content-Type": "application/json"},
    )

    assert resp.status_code == 201
    assert resp.headers["say"] == "hello"
    assert resp.data == b'{"foo": "bar"}'
    assert resp.headers["Content-Type"] == "flask-classful/default"


def test_representation_with_default():
    """Default representation should not override proper match"""
    resp = client.post(
        "/default/", data=json.dumps({"foo": "bar"}), headers=input_headers
    )

    assert resp.status_code == 201
    assert resp.headers["say"] == "hello"
    assert resp.data == b'{"foo": "bar"}'
    assert resp.headers["Content-Type"] == "application/json"
