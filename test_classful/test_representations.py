from flask import Flask, make_response, redirect
from flask_classful import FlaskView
import json
from nose.tools import *


def output_json(data, code, headers=None):
    content_type = 'application/json'
    dumped = json.dumps(data)
    if headers:
        headers.update({'Content-Type': content_type})
    else:
        headers = {'Content-Type': content_type}
    response = make_response(dumped, code, headers)
    return response


# Test Responses
response_1 = {
    'internal_string':"just a string",
    'integer': 5,
    'validate_int': 1,
    'input_required': 'just another string'
}
response_2 = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'Nothing'
}
response_get = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'GET'
}
response_put = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'PUT'
}
response_post = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'POST'
}
response_delete = {
    'internal_string':"What is going on",
    'integer': 3,
    'validate_int': 1,
    'input_required': 'DELETE'
}

input_headers = [('Content-Type', 'application/json')]
input_data = {'input_required': 'required'}


class RepresentationView(FlaskView):
    representations = {'application/json': output_json}
    base_args = ['fields']


    def index(self):
        return [response_1, response_2]

    def get(self, obj_id):
        return response_get

    def put(self, obj_id):
        return response_put, 403

    def post(self):
        return response_post, 404, {'say': 'hello'}

    def delete(self, obj_id):
        return response_delete

    def redirect(self):
        return redirect("http://google.com")

app = Flask("representations")
RepresentationView.register(app)

client = app.test_client()

def test_index_representation():
    resp = client.get("/representation/")
    eq_(json.dumps([response_1, response_2]), resp.data.decode('ascii'))

def test_get_representation():
    resp = client.get("/representation/1")
    eq_(json.dumps(response_get), resp.data.decode('ascii'))

def test_post_representation():
    resp = client.post("/representation/", headers=input_headers, data=json.dumps(input_data))
    eq_(resp.status_code, 404, 'should return 404 status code')
    eq_(resp.headers['say'], 'hello')
    eq_(json.dumps(response_post), resp.data.decode('ascii'))

def test_put_representation():
    resp = client.put("/representation/1", headers=input_headers, data=json.dumps(input_data))
    eq_(resp.status_code, 403, 'should return 403 status code')
    eq_(json.dumps(response_put), resp.data.decode('ascii'))

def test_delete_representation():
    resp = client.delete("/representation/1")
    eq_(json.dumps(response_delete), resp.data.decode('ascii'))

def test_skip_representation_matching_if_response_is_returned():
    resp = client.get("/representation/redirect/")
    assert resp.status_code == 302
    assert resp.location == "http://google.com"
