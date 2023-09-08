Flask-Classful
==============

Flask-Classful is an extension that adds class-based views to [Flask][].
Class-based views are a way to encapsulate specific context and behavior for
routes and methods, complementing Flask's blueprints. They provide a more
powerful system than Flask's own `MethodView`.

Read the documentation at <https://flask-classful.readthedocs.io>.

[Flask]: https://flask.palletsprojects.com


Pallets Community Ecosystem
---------------------------

> [!IMPORTANT]\
> This project is part of the Pallets Community Ecosystem. Pallets is the
> organization that maintains Flask; Pallets-Eco enables community maintenance
> of Flask extensions. If you are interested in helping maintain this project,
> please reach out on [the Pallets Discord server](https://discord.gg/pallets).


A Basic Example
---------------

This example defines a few routes by defining methods on a subclass of
`flask_classful.FlaskView`.

```python
# example.py
import random
from flask import Flask, abort
from flask_classful import FlaskView

quotes = [
    "A noble spirit embiggens the smallest man! ~ Jebediah Springfield",
    "If there is a way to do it better... find it. ~ Thomas Edison",
    "No one knows what he can do till he tries. ~ Publilius Syrus"
]

app = Flask(__name__)

class QuotesView(FlaskView):
    def index(self):
        return "<br>".join(quotes)

    def get(self, id):
        id = int(id)

        if id < len(quotes):
            return quotes[id]

        abort(404)

    def random(self):
        return random.choice(quotes)

QuotesView.register(app)
```

```
$ flask -A example run --debug
```

-   http://127.0.0.1:5000/quotes/ shows all the quotes.
-   http://127.0.0.1:5000/quotes/1/ shows a single quote.
-   http://127.0.0.1:5000/quotes/random/ shows a random quote.


Forked from Flask-Classy
------------------------

> [!NOTE]\
> This is a fork of Flask-Classy to continue development after it was not
> updated for a long time.
