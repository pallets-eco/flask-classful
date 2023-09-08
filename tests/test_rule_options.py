from unittest.mock import patch

from flask import Flask

from .view_classes import BasicView


@patch("flask.Flask.add_url_rule")
def test_rule_options(rule):
    app = Flask("rules_options", static_folder=None)
    BasicView.register(app, strict_slashes=False)

    client = app.test_client()
    client.get("/basic/")

    for args, kwargs in rule.call_args_list:
        assert kwargs.get("strict_slashes") is False, (args, kwargs)
