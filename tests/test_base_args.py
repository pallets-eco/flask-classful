from flask import Flask
from flask import jsonify
from pytest import raises

from flask_classful import FlaskView

app = Flask(__name__)
app.config["DEBUG"] = True


class NoRouteBaseArgsView(FlaskView):
    route_base = "/route/without/args"

    def get(self, arg_1):
        return (
            jsonify(
                {
                    "arg_1": arg_1,
                }
            ),
            200,
        )


class MultiRouteBaseArgsView(FlaskView):
    route_base = "/route/<arg_1>/with/<arg_2>/some_args"

    def get(self, arg_1, arg_2, arg_3):
        return (
            jsonify(
                {
                    "arg_1": arg_1,
                    "arg_2": arg_2,
                    "arg_3": arg_3,
                }
            ),
            200,
        )


class OtherRouteBaseArgsView(FlaskView):
    route_base = "/route/<arg_1>/other"

    def get(self, arg_1, arg_2):
        return (
            jsonify(
                {
                    "arg_1": arg_1,
                    "arg_2": arg_2,
                }
            ),
            200,
        )


class ErroneousRouteBaseArgsView(FlaskView):
    route_base = "/route/<arg_1>/error"

    def get(self, arg_2):
        return (
            jsonify(
                {
                    "arg_2": arg_2,
                }
            ),
            200,
        )


NoRouteBaseArgsView.register(app)
MultiRouteBaseArgsView.register(app)
OtherRouteBaseArgsView.register(app)
ErroneousRouteBaseArgsView.register(app)


def test_no_route_args():
    _, base_args = NoRouteBaseArgsView.get_route_base()
    # No route base with args == no base args
    assert base_args == set()
    client = app.test_client()
    resp = client.get("/route/without/args/foo/")
    assert resp.status_code == 200
    assert resp.json == {"arg_1": "foo"}


def test_route_args_are_detected():
    _, base_args = MultiRouteBaseArgsView.get_route_base()
    assert base_args == {"arg_1", "arg_2"}


def test_multi_route_args_values():
    client = app.test_client()
    resp = client.get("/route/foo/with/bar/some_args/baz/")
    assert resp.status_code == 200
    assert resp.json == {"arg_1": "foo", "arg_2": "bar", "arg_3": "baz"}


def test_route_args_are_independent_across_views():
    _, base_args = OtherRouteBaseArgsView.get_route_base()
    # arg_2 does not leak from evaluating the previous view
    assert base_args == {"arg_1"}


def test_missing_base_arg_in_method():
    _, base_args = ErroneousRouteBaseArgsView.get_route_base()
    # Base arg is recognized
    assert base_args == {"arg_1"}
    # Rule is correctly generated
    assert (
        ErroneousRouteBaseArgsView.build_rule("/", ErroneousRouteBaseArgsView.get)
        == ErroneousRouteBaseArgsView.route_base + "/<arg_2>"
    )
    client = app.test_client()
    # But calling the method fails because ErroneousRouteBaseArgsView.get is
    # supplied with an unexpected "arg_1" argument
    with raises(TypeError):
        client.get("/route/foo/error/baz/")
