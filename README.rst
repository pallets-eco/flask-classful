Flask-Classful
==============

Note::

    This is a fork of original `Flask-Classy` for continuing its development since the original
    project was not updated for a long time. For more information, see:
    https://github.com/apiguy/flask-classy/issues/80


Flask-Classful is an extension that adds class-based views to Flask.
But why?

I ❤ Flask. Like a lot. But sometimes projects get a little big
and I need some way of managing and organizing all the different
pieces. I know what you're saying: "But what about Blueprints?"

You're right. Blueprints are pretty awesome. But I found that they
aren't always enough to encapsulate a specific context the way I
need. What I wanted, no what I *needed* was to be able to group
my views into relevant classes each with their own context and
behavior. It's also made testing really nifty too.

"OK, I see your point. But can't I just use the base classes in
``flask.views`` to do that?"

Well, yes and no. While ``flask.views.MethodView`` does
provide some of the functionality of ``flask_classful.FlaskView``
it doesn't quite complete the picture by supporting methods that
aren't part of the typical CRUD operations for a given resource, or
make it easy for me to override the route rules for particular view.
And while ``flask.views.View`` does add some context, it requires
a class for each view instead of letting me group very similar
views for the same resource into a single class.

"But my projects aren't that big. Can Flask-Classful do
anything else for me besides making a big project easier to manage?"

Why yes. It does help a bit with some other things.

For example, `Flask-Classful` will automatically generate routes based on the methods
in your views, and makes it super simple to override those routes
using Flask's familiar decorator syntax.

.. _Flask-Classful: https://github.com/pallets-eco/flask-classful
.. _Flask: https://flask.palletsprojects.com/

Installation
------------

Install the latest extension with::

    $ pip install flask-classful


Let's see how it works
----------------------

If you're like me, you probably get a better idea of how to use something
when you see it being used. Let's go ahead and create a little app to
see how Flask-Classful works:

..  code-block:: python

    from flask import Flask
    from flask_classful import FlaskView

    # we'll make a list to hold some quotes for our app
    quotes = [
        "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
        "If there is a way to do it better... find it. ~ Thomas Edison",
        "No one knows what he can do till he tries. ~ Publilius Syrus"
    ]

    app = Flask(__name__)

    class QuotesView(FlaskView):
        def index(self):
            return "<br>".join(quotes)

    QuotesView.register(app)

    if __name__ == '__main__':
        app.run()

Run this app and open your web browser to: http://localhost:5000/quotes/

As you can see, it returns the list of quotes. But what if we just wanted
one quote? What would we do then?

..  code-block:: python

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            id = int(id)
            if id < len(quotes):
                return quotes[id]
            else:
                return "Not Found", 404

Now direct your browser to: http://localhost:5000/quotes/1/ and you should
see the very poignant quote from the esteemed Mr. Edison.

That's cool and all, but what if we just wanted a random quote? What then?
Let's add a random view to our FlaskView:

..  code-block:: python

    from random import choice

..  code-block:: python

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            ...

        def random(self):
            return choice(quotes)

And point your browser to: http://localhost:5000/quotes/random/ and see
that a random quote is returned each time. Voilà!

So by now you must be keenly aware of the fact that you have not defined a
single route, but yet routing is obviously taking place. "Is this voodoo?"
you ask?

Not at all. Flask-Classful will automatically create routes for any method
in a FlaskView that doesn't begin with an underscore character.
You can still define your own routes of course, and we'll look at that next.
