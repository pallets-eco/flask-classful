Release Steps
=============

Follow: http://dev.teracy.org/docs/release_process.html

Next iteration
--------------

Update next iteration for develop branch:
- flask_classful.py
- docs/conf.py


CHANGELOG.md
------------

update the change log


flask_classful.py
-----------------

update this line for the right version:
::

  __version__ = "0.7.0-dev0"


docs/conf.py
------------

update these lines for the right versions:
::
  # The short X.Y version.
  version = '0.7'
  # The full version, including alpha/beta/rc tags.
  release = '0.7.0'

Upload the tagged version to PyPI
---------------------------------

```
$ git checkout vX.X.X
$ python setup.py sdist bdist_wheel --universal
$ twine upload dist/*
```

Ref:
- http://python-packaging-user-guide.readthedocs.io/en/latest/distributing/
- https://github.com/pypa/twine
