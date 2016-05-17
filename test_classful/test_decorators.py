from flask import Flask, url_for
from .view_classes import DecoratedView
from .view_classes import DecoratedBoldListView
from .view_classes import DecoratedBoldItalicsListView
from .view_classes import DecoratedListMemberView
from .view_classes import DecoratedListFunctionAttributesView
from .view_classes import DecoratedListMemberFunctionAttributesView
from nose.tools import *

app = Flask("decorated")
DecoratedView.register(app)
DecoratedBoldListView.register(app)
DecoratedBoldItalicsListView.register(app)
DecoratedListMemberView.register(app)
DecoratedListFunctionAttributesView.register(app)
DecoratedListMemberFunctionAttributesView.register(app)
client = app.test_client()


def test_func_decorator_index():
    resp = client.get('/decorated/')
    eq_(b"Index", resp.data)


def test_func_decorator_get():
    resp = client.get('/decorated/1234')
    eq_(b"Get 1234", resp.data)


def test_recursive_decorator_post():
    resp = client.post('/decorated/')
    eq_(b"Post", resp.data)


def test_more_recursive_decorator_get():
    resp = client.get('/decorated/get_some/')
    eq_(b"Get Some", resp.data)


def test_multiple_recursive_decorators_get():
    resp = client.get('/decorated/get_this/')
    eq_(b"Get This", resp.data)


def test_routes_with_recursive_decorators():
    resp = client.get('/decorated/mixitup/')
    eq_(b"Mix It Up", resp.data)


def test_recursive_with_parameter():
    resp = client.get('/decorated/someval/1234')
    eq_(b"Someval 1234", resp.data)


def test_recursive_with_route_with_parameter():
    resp = client.get('/decorated/anotherval/1234')
    eq_(b"Anotherval 1234", resp.data)


def test_params_decorator():
    resp = client.get('/decorated/params_decorator_method/')
    eq_(b"Params Decorator", resp.data)


def test_params_decorator_delete():
    resp = client.delete('/decorated/1234')
    eq_(b"Params Decorator Delete 1234", resp.data)


def test_decorator_bold_list_get():
    '''Tests that the get route is wrapped in bold'''
    resp = client.get('/decorated_bold_list_view/1234')
    eq_(b'<b>' in resp.data, True)
    eq_(b'</b>' in resp.data, True)


def test_decorator_bold_list_index():
    '''Tests that the index route is wrapped in bold'''
    resp = client.get('/decorated_bold_list_view/')
    eq_(b'<b>' in resp.data, True)
    eq_(b'</b>' in resp.data, True)


def test_decorator_bold_italics_list_get():
    '''Tests that the get route is wrapped in bold and italics'''
    resp = client.get('/decorated_bold_italics_list_view/1234')
    eq_(b'<i>' in resp.data, True)
    eq_(b'</i>' in resp.data, True)
    eq_(b'<b>' in resp.data, True)
    eq_(b'</b>' in resp.data, True)


def test_decorator_bold_italics_list_index():
    '''Tests that the index route is wrapped in bold and italics'''
    resp = client.get('/decorated_bold_italics_list_view/')
    eq_(b'<i>' in resp.data, True)
    eq_(b'</i>' in resp.data, True)
    eq_(b'<b>' in resp.data, True)
    eq_(b'</b>' in resp.data, True)


def test_decorator_list_member_index():
    '''
    Tests that the index route is wrapped in bold,
    italics and paragraph
    '''
    resp = client.get('/decorated_list_member_view/')
    eq_(b'<i>' in resp.data, True)
    eq_(b'</i>' in resp.data, True)
    eq_(b'<b>' in resp.data, True)
    eq_(b'</b>' in resp.data, True)
    eq_(b'<p>' not in resp.data, True)
    eq_(b'</p>' not in resp.data, True)


def test_decorator_list_member_get():
    '''Tests the ordering of decorators'''
    resp = client.get('/decorated_list_member_view/1234')
    eq_(b'<b>', resp.data[:3])
    eq_(b'<i>', resp.data[3:6])
    eq_(b'<p>', resp.data[6:9])
    eq_(b'</p>', resp.data[-12:-8])
    eq_(b'</i>', resp.data[-8:-4])
    eq_(b'</b>', resp.data[-4:])


def test_decorator_list_function_attributes_get():
    '''Verify list of decorators with attributes modify all functions in FlaskView'''
    resp = client.get('/decorated_list_function_attributes_view/1234')
    eq_(b'Get 1234' in resp.data, True)
    eq_(hasattr(app.view_functions['DecoratedListFunctionAttributesView:get'], 'eggs'), True)
    eq_('scrambled', app.view_functions['DecoratedListFunctionAttributesView:get'].eggs)


def test_decorator_list_function_attributes_index():
    '''Verify list of decorators with attributes modify all functions in FlaskView'''
    resp = client.get('/decorated_list_function_attributes_view/')
    eq_(b'Index' in resp.data, True)
    eq_(hasattr(app.view_functions['DecoratedListFunctionAttributesView:index'], 'eggs'), True)
    eq_('scrambled', app.view_functions['DecoratedListFunctionAttributesView:index'].eggs)


def test_decorator_list_member_function_attributes_get():
    '''Verify decorator with attributes does not modify other members'''
    resp = client.get('/decorated_list_member_function_attributes_view/4321')
    eq_(b'Get 4321' in resp.data, True)
    eq_(hasattr(app.view_functions['DecoratedListMemberFunctionAttributesView:get'], 'eggs'), False)


def test_decorator_list_member_function_attributes_index():
    '''Verify decorator with attributes modify decorated memeber functions'''
    resp = client.get('/decorated_list_member_function_attributes_view/')
    eq_(b'Index' in resp.data, True)
    eq_(hasattr(app.view_functions['DecoratedListMemberFunctionAttributesView:index'], 'eggs'), True)
    eq_('scrambled', app.view_functions['DecoratedListMemberFunctionAttributesView:index'].eggs)
