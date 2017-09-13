import json

from flask import Flask
from flask_classful import FlaskView
from webargs.flaskparser import use_args
from webargs import fields
from nose.tools import eq_

# we'll make a list to hold some quotes for our app
quotes = [
    "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
    "If there is a way to do it better... find it. ~ Thomas Edison",
    "No one knows what he can do till he tries. ~ Publilius Syrus"
]

app = Flask(__name__)
app.config['DEBUG'] = True

put_args = {
    "text": fields.Str(required=True)
}


class QuotesView(FlaskView):
    base_args = ['args']

    def index(self):
        return "<br>".join(quotes)

    def get(self, id):
        quote_id = int(id)
        if quote_id < len(quotes) - 1:
            return quotes[quote_id]
        else:
            return "Not Found", 404

    @use_args(put_args)
    def put(self, args, id):
        quote_id = int(id)
        if quote_id >= len(quotes) - 1:
            return "Not Found", 404
        quotes[quote_id] = args['text']
        return quotes[quote_id]


class UglyNameView(FlaskView):
    base_args = ['args']
    route_base = 'quotes-2'

    def index(self):
        return "<br>".join(quotes)

    def get(self, id):
        quote_id = int(id)
        if quote_id < len(quotes) - 1:
            return quotes[quote_id]
        else:
            return "Not Found", 404

    @use_args(put_args)
    def put(self, args, id):
        quote_id = int(id)
        if quote_id >= len(quotes) - 1:
            return "Not Found", 404
        quotes[quote_id] = args['text']
        return quotes[quote_id]


QuotesView.register(app)
UglyNameView.register(app)

client = app.test_client()

input_headers = [('Content-Type', 'application/json')]
input_data = {'text': 'My quote'}


def test_quotes_index():
    resp = client.get("/quotes/")
    num = len(str(resp.data).split("<br>"))
    eq_(3, num)
    resp = client.get("/quotes")
    eq_(resp.status_code, 301)


def test_quotes_get():
    resp = client.get("/quotes/0/")
    eq_(quotes[0], resp.data.decode('ascii'))


def test_quotes_put():
    resp = client.put("/quotes/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    eq_(input_data["text"], resp.data.decode('ascii'))


def test_quotes2_index():
    resp = client.get("/quotes-2/")
    num = len(str(resp.data).split("<br>"))
    eq_(3, num)
    resp = client.get("/quotes")
    eq_(resp.status_code, 301)


def test_quotes2_get():
    resp = client.get("/quotes-2/0/")
    eq_(quotes[0], resp.data.decode('ascii'))
    eq_(UglyNameView.base_args.count(UglyNameView.route_base), 1)


def test_quotes2_put():
    resp = client.put("/quotes-2/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    eq_(input_data["text"], resp.data.decode('ascii'))
    eq_(UglyNameView.base_args.count(UglyNameView.route_base), 1)

# see: https://github.com/teracyhq/flask-classful/pull/56#issuecomment-328985183
def test_unique_elements():
    client.put("/quotes-2/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    eq_(UglyNameView.base_args.count(UglyNameView.route_base), 1)

