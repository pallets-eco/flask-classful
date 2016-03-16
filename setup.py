"""
Flask-Classful
--------------

Class based views for Flask
"""
import os
import re
from setuptools import setup, find_packages


def get_file(*parts):
    """
    Gets a file and open it
    """
    filename = os.path.join(os.path.dirname(__file__), *parts)
    return open(filename)


def find_version(*file_paths):
    """
    Finds version from the provided file_paths
    """
    got_file = get_file(*file_paths)
    for line in got_file:
        if re.match('__version__ = .+', line):
            return re.search(r'\d.+\d', line).group(0)
    raise RuntimeError('Unable to find string version')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='Flask-Classful',
    version=find_version('flask_classful.py'),
    url='https://github.com/teracyhq/flask-classful',
    license='BSD',
    author='Freedom Dumlao & Teracy, Inc',
    author_email='teracyhq@teracy.com',
    description='Class based views for Flask',
    long_description=__doc__,
    py_modules=['flask_classful'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_classful'
)
