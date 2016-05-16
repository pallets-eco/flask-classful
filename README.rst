Flask-Classful
==============

..  image:: https://travis-ci.org/teracyhq/flask-classful.svg?branch=develop
    :target: https://travis-ci.org/teracyhq/flask-classful

..  image:: https://badges.gitter.im/teracyhq/flask-classful.svg
    :alt: Join the chat at https://gitter.im/teracyhq/flask-classful
    :target: https://gitter.im/teracyhq/flask-classful?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

..  image:: https://coveralls.io/repos/teracyhq/flask-classful/badge.svg?branch=develop&service=github
    :target: https://coveralls.io/github/teracyhq/flask-classful?branch=master

..  image:: https://img.shields.io/pypi/v/Flask-Classful.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/Flask-Classful
    :alt: 'Latest PyPI release'

..  image:: https://img.shields.io/pypi/wheel/flask-classful.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/Flask-Classful
    :alt: 'Wheel Supported'

..  image:: https://img.shields.io/pypi/pyversions/flask-classful.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/Flask-Classful
    :alt: 'Supported Python versions'

|

..  image:: https://www.quantifiedcode.com/api/v1/project/1f655f7956a24d9fbf787ec149cbcf5a/badge.svg
    :target: https://www.quantifiedcode.com/app/project/1f655f7956a24d9fbf787ec149cbcf5a
    :alt: Code Issues

..  image:: https://img.shields.io/github/issues/teracyhq/flask-classful.svg
    :target: https://waffle.io/teracyhq/flask-classful
    :alt: Open Issues

..  image:: https://badge.waffle.io/teracyhq/flask-classful.svg?label=sprint-current&title=Current%20Sprint
    :target: https://waffle.io/teracyhq/flask-classful
    :alt: 'Current Sprint'

..  image:: https://badge.waffle.io/teracyhq/flask-classful.svg?label=in%20progress&title=In%20Progress
    :target: https://waffle.io/teracyhq/flask-classful
    :alt: 'In Progress'

..  image:: https://badge.waffle.io/teracyhq/flask-classful.svg?label=under-review&title=Under%20Review
    :target: https://waffle.io/teracyhq/flask-classful
    :alt: 'Under Review'

..  image:: https://graphs.waffle.io/teracyhq/flask-classful/throughput.svg
    :target: https://waffle.io/teracyhq/flask-classful/metrics/throughput
    :alt: 'Throughput Graph'

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

.. _Flask-Classful: http://github.com/teracyhq/flask-classful
.. _Flask: http://flask.pocoo.org/

Installation
------------

Install the latest extension with::

    $ pip install flask-classful

Or install the bleeding edge development version with::

    $ pip install git+https://github.com/teracyhq/flask-classful.git@develop#egg=flask-classful


Let's see how it works
----------------------

If you're like me, you probably get a better idea of how to use something
when you see it being used. Let's go ahead and create a little app to
see how Flask-Classful works::

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

::

    class QuotesView(FlaskView):
        def index(self):
            ...

        def get(self, id):
            id = int(id)
            if id < len(quotes) - 1:
                return quotes[id]
            else:
                return "Not Found", 404

Now direct your browser to: http://localhost:5000/quotes/1/ and you should
see the very poignant quote from the esteemed Mr. Edison.

That's cool and all, but what if we just wanted a random quote? What then?
Let's add a random view to our FlaskView::

    from random import choice

::

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



Questions?
----------

Feel free to ping me on twitter @teracyhq, or head on over to the
github repo at http://github.com/teracyhq/flask-classful so you can join
the fun.


License
-------

BSD License
::

    Copyright (c) 2016 by Teracy, Inc. and individual contributors.
    All rights reserved.

    Copyright (c) 2012 by Freedom Dumlao.
    Some rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

        1. Redistributions of source code must retain the above copyright notice,
           this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright
           notice, this list of conditions and the following disclaimer in the
           documentation and/or other materials provided with the distribution.

        3. Neither the name of Teracy, Inc. nor the names of its contributors may be used
           to endorse or promote products derived from this software without
           specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

