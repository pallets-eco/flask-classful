from flask import Flask, make_response
from flask_classy import FlaskView
import json
from nose.tools import *


def output_json(data, code, headers=None):
    content_type = 'application/json'
    dumped = json.dumps(data)
    response = make_response(dumped, code)
    if headers:
        headers.extend({'Content-Type': content_type})
    else:
        headers = {'Content-Type': content_type}
    response.headers.extend(headers)

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

headers = [('Content-Type', 'application/json')]
data = {'input_required': 'required'}


class RepresentationView(FlaskView):
    representations = {'application/json': output_json}
    base_args = ['fields']


    def index(self):
        return [response_1, response_2]

    def get(self, obj_id):
        return response_get

    def put(self, obj_id):
        return response_put

    def post(self):
        return response_post

    def delete(self, obj_id):
        return response_delete

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
    resp = client.post("/representation/", headers=headers, data=json.dumps(data))
    eq_(json.dumps(response_post), resp.data.decode('ascii'))

def test_put_representation():
    resp = client.put("/representation/1", headers=headers, data=json.dumps(data))
    eq_(json.dumps(response_put), resp.data.decode('ascii'))

def test_delete_representation():
    resp = client.delete("/representation/1")
    eq_(json.dumps(response_delete), resp.data.decode('ascii'))
