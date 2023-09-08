from flask import Flask
from .view_classes import WithInitArgument, WithoutInitArgument
import json

app = Flask("init_argument")
WithInitArgument.register(app, init_argument = "fistro de la praderarrr")
WithoutInitArgument.register(app)

client = app.test_client()


def test_init_argument_used():
    resp = client.get("/with_init_argument/")
    assert "fistro de la praderarrr" == json.loads(resp.data.decode('utf-8'))["init_argument"]
    assert resp.status_code == 200


def test_init_argument_not_used():
    resp = client.get("/without_init_argument/")
    assert "not sent" == json.loads(resp.data.decode('utf-8'))["init_argument"]
    assert resp.status_code == 200
