from flask import Flask

from .view_classes import DecoratedAppendClassAttributeView
from .view_classes import DecoratedBoldItalicsListView
from .view_classes import DecoratedBoldListView
from .view_classes import DecoratedListFunctionAttributesView
from .view_classes import DecoratedListMemberFunctionAttributesView
from .view_classes import DecoratedListMemberView
from .view_classes import DecoratedView

app = Flask("decorated")
DecoratedView.register(app)
DecoratedBoldListView.register(app)
DecoratedBoldItalicsListView.register(app)
DecoratedListMemberView.register(app)
DecoratedListFunctionAttributesView.register(app)
DecoratedListMemberFunctionAttributesView.register(app)
DecoratedAppendClassAttributeView.register(app)
client = app.test_client()


def test_func_decorator_index():
    resp = client.get("/decorated/")
    assert b"Index" == resp.data
    resp = client.get("/decorated")
    assert resp.status_code == 308


def test_func_decorator_get():
    resp = client.get("/decorated/1234/")
    assert b"Get 1234" == resp.data
    resp = client.get("/decorated/1234")
    assert resp.status_code == 308


def test_recursive_decorator_post():
    resp = client.post("/decorated/")
    assert b"Post" == resp.data
    resp = client.post("/decorated")
    assert resp.status_code == 308


def test_more_recursive_decorator_get():
    resp = client.get("/decorated/get_some/")
    assert b"Get Some" == resp.data
    resp = client.get("/decorated/get_some")
    assert resp.status_code == 308


def test_multiple_recursive_decorators_get():
    resp = client.get("/decorated/get_this/")
    assert b"Get This" == resp.data
    resp = client.get("/decorated/get_this")
    assert resp.status_code == 308


def test_routes_with_recursive_decorators():
    resp = client.get("/decorated/mixitup/")
    assert b"Mix It Up" == resp.data
    resp = client.get("/decorated/mixitup")
    assert resp.status_code == 308


def test_recursive_with_parameter():
    resp = client.get("/decorated/someval/1234/")
    assert b"Someval 1234" == resp.data


def test_recursive_with_route_with_parameter():
    resp = client.get("/decorated/anotherval/1234/")
    assert b"Anotherval 1234" == resp.data


def test_params_decorator():
    resp = client.get("/decorated/params_decorator_method/")
    assert b"Params Decorator" == resp.data


def test_params_decorator_delete():
    resp = client.delete("/decorated/1234/")
    assert b"Params Decorator Delete 1234" == resp.data
    resp = client.delete("/decorated/1234")
    assert resp.status_code == 308


def test_decorator_bold_list_get():
    """Tests that the get route is wrapped in bold"""
    resp = client.get("/decorated_bold_list_view/1234/")
    assert b"<b>" in resp.data
    assert b"</b>" in resp.data
    assert b"<b>Get 1234</b>" == resp.data
    resp = client.get("/decorated_bold_list_view/1234")
    assert resp.status_code == 308


def test_decorator_bold_list_index():
    """Tests that the index route is wrapped in bold"""
    resp = client.get("/decorated_bold_list_view/")
    assert b"<b>" in resp.data
    assert b"</b>" in resp.data
    assert b"<b>Index</b>" == resp.data


def test_decorator_bold_italics_list_get():
    """Tests that the get route is wrapped in bold and italics"""
    resp = client.get("/decorated_bold_italics_list_view/1234/")
    assert b"<i>" in resp.data
    assert b"</i>" in resp.data
    assert b"<b>" in resp.data
    assert b"</b>" in resp.data
    assert b"<b><i>Get 1234</i></b>" == resp.data
    resp = client.get("/decorated_bold_italics_list_view/1234")
    assert resp.status_code == 308


def test_decorator_bold_italics_list_index():
    """Tests that the index route is wrapped in bold and italics"""
    resp = client.get("/decorated_bold_italics_list_view/")
    assert b"<i>" in resp.data
    assert b"</i>" in resp.data
    assert b"<b>" in resp.data
    assert b"</b>" in resp.data
    assert b"<b><i>Index</i></b>" == resp.data


def test_decorator_list_member_index():
    """
    Tests that the index route is wrapped in bold,
    italics and paragraph
    """
    resp = client.get("/decorated_list_member_view/")
    assert b"<i>" in resp.data
    assert b"</i>" in resp.data
    assert b"<b>" in resp.data
    assert b"</b>" in resp.data
    assert b"<p>" not in resp.data
    assert b"</p>" not in resp.data
    assert b"<b><i>Index</i></b>" == resp.data


def test_decorator_list_member_get():
    """Tests the ordering of decorators"""
    resp = client.get("/decorated_list_member_view/1234/")
    assert b"<b>" == resp.data[:3]
    assert b"<i>" == resp.data[3:6]
    assert b"<p>" == resp.data[6:9]
    assert b"</p>" == resp.data[-12:-8]
    assert b"</i>" == resp.data[-8:-4]
    assert b"</b>" == resp.data[-4:]
    assert b"<b><i><p>Get 1234</p></i></b>" == resp.data
    resp = client.get("/decorated_list_member_view/1234")
    assert resp.status_code == 308


def test_decorator_list_function_attributes_get():
    """
    Verify list of decorators with attributes modify all functions in FlaskView
    """
    resp = client.get("/decorated_list_function_attributes_view/1234/")
    assert b"Get 1234" in resp.data
    assert b"<i><b>Get 1234</b></i>" == resp.data
    assert hasattr(
        app.view_functions["DecoratedListFunctionAttributesView:get"], "eggs"
    )
    assert (
        "scrambled"
        == app.view_functions["DecoratedListFunctionAttributesView:get"].eggs
    )
    resp = client.get("/decorated_list_function_attributes_view/1234")
    assert resp.status_code == 308


def test_decorator_list_function_attributes_index():
    """
    Verify list of decorators with attributes modify all functions in FlaskView
    """
    resp = client.get("/decorated_list_function_attributes_view/")
    assert b"Index" in resp.data
    assert b"<i>Index</i>" == resp.data
    assert hasattr(
        app.view_functions["DecoratedListFunctionAttributesView:index"], "eggs"
    )
    assert (
        "scrambled"
        == app.view_functions["DecoratedListFunctionAttributesView:index"].eggs
    )


def test_decorator_list_member_function_attributes_get():
    """Verify decorator with attributes does not modify other members"""
    resp = client.get("/decorated_list_member_function_attributes_view/4321/")
    assert b"Get 4321" in resp.data
    assert b"<i><b>Get 4321</b></i>" == resp.data
    assert (
        hasattr(
            app.view_functions["DecoratedListMemberFunctionAttributesView:get"], "eggs"
        )
        is False
    )
    resp = client.get("/decorated_list_member_function_attributes_view/4321")
    assert resp.status_code == 308


def test_decorator_list_member_function_attributes_index():
    """Verify decorator with attributes modify decorated memeber functions"""
    resp = client.get("/decorated_list_member_function_attributes_view/")
    assert b"Index" in resp.data
    assert b"<i>Index</i>" == resp.data
    assert hasattr(
        app.view_functions["DecoratedListMemberFunctionAttributesView:index"], "eggs"
    )
    assert (
        "scrambled"
        == app.view_functions["DecoratedListMemberFunctionAttributesView:index"].eggs
    )


def test_decorator_append_class_attribute_index():
    resp = client.get("/decorated_append_class_attribute_view/")
    assert b"Index (this is a test)" == resp.data
