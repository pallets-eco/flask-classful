import json
import marshmallow as ma

from flask import Flask
from flask_classful import FlaskView, route
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from webargs import fields

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


class UserSchema(Schema):
    email = ma.fields.Str()

    class Meta:
        strict = True


def make_user_schema(request):
    # Filter based on 'fields' query parameter
    only = request.args.get("fields", None)
    # Respect partial updates for PATCH requests
    partial = request.method == "PATCH"
    # Add current request to the schema's context
    return UserSchema(only=only, partial=partial, context={"request": request})


class UsersView(FlaskView):
    base_args = ['args']

    @use_args(make_user_schema)
    def post(self, args):
        return args['email']

    @use_args(make_user_schema)
    def put(self, args, id):
        return args['email']

    @use_args(make_user_schema)
    def patch(self, args, id):
        return args['email']


class QuoteSchema(ma.Schema):
    id = ma.fields.Int()
    text = ma.fields.Str()

    class Meta:
        strict = True


def make_quote_schema(request):
    # Filter based on 'fields' query parameter
    only = request.args.get("fields", None)
    # Respect partial updates for PATCH requests
    partial = request.method == "PATCH"
    # Add current request to the schema's context
    return QuoteSchema(only=only, partial=partial, context={"request": request})


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

    @route("<id>/", methods=['PATCH'])
    @use_args(make_quote_schema)
    def factory(self, args, id):
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
UsersView.register(app)

client = app.test_client()

input_headers = [('Content-Type', 'application/json')]
input_data = {'text': 'My quote'}


def test_users_post():
    resp = client.post('users/', headers=input_headers, data=json.dumps({'email':'test@example.com'}))
    assert resp.status_code == 200
    assert "test@example.com" == resp.data.decode('ascii')

def test_users_put():
    resp = client.put('users/1/', headers=input_headers, data=json.dumps({'email':'test@example.com'}))
    assert resp.status_code == 200
    assert "test@example.com" == resp.data.decode('ascii')

def test_users_patch():
    resp = client.patch('users/1/', headers=input_headers, data=json.dumps({'email':'test@example.com'}))
    assert resp.status_code == 200
    assert "test@example.com" == resp.data.decode('ascii')

def test_quotes_index():
    resp = client.get("/quotes/")
    num = len(str(resp.data).split("<br>"))
    assert 3 == num
    resp = client.get("/quotes")
    assert resp.status_code == 308


def test_quotes_get():
    resp = client.get("/quotes/0/")
    assert quotes[0] == resp.data.decode('ascii')


def test_quotes_put():
    resp = client.put("/quotes/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    assert input_data["text"] == resp.data.decode('ascii')

def test_quotes_factory():
    resp = client.patch("/quotes/1/",
                        headers=input_headers,
                        data=json.dumps(input_data))
    assert input_data["text"] == resp.data.decode('ascii')

def test_quotes2_index():
    resp = client.get("/quotes-2/")
    num = len(str(resp.data).split("<br>"))
    assert 3 == num
    resp = client.get("/quotes-2")
    assert resp.status_code == 308


def test_quotes2_get():
    resp = client.get("/quotes-2/0/")
    assert quotes[0] == resp.data.decode('ascii')
    assert UglyNameView.base_args.count(UglyNameView.route_base) == 0


def test_quotes2_put():
    resp = client.put("/quotes-2/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    assert input_data["text"] == resp.data.decode('ascii')
    assert UglyNameView.base_args.count(UglyNameView.route_base) == 0

# see: https://github.com/pallets-eco/flask-classful/pull/56#issuecomment-328985183
def test_unique_elements():
    client.put("/quotes-2/1/",
                      headers=input_headers,
                      data=json.dumps(input_data))
    assert UglyNameView.base_args.count(UglyNameView.route_base) == 0
