# flask-classful dev-setup

Please follow this getting started guide to set up the development environment.

Please take a cup of coffee with you, you mostly don't have to do anything but wait for the result, enjoy!


## Setting up from scratch

### Setting up teracy-dev

- Please follow document at https://github.com/teracyhq/dev-setup/blob/develop/README.md to set up teracy-dev and dev-setup, then come back here to set up the `flask-clasful` project.


### Setting up flask-classful

Stop the watching files by using `Ctrl + c`.

- Fork the `flask-classful` repository into your github account.
- Clone the forked `flask-classful` repo into the `~/teracy-dev/workspace` directory.

    ```bash
    $ cd ~/teracy-dev/workspace/
    $ git clone <your_forked_repository_here> flask-classful
    $ cd flask-classful
    $ git remote add upstream git@github.com:teracyhq/flask-classful.git
    ```

- Note that you should always sync the `dev-setup` repository along with `teracy-dev`. After changed, `$ vagrant reload --provision` should get the new configuration updated into the VM. Or `$ vagrant destroy` and `$ vagrant up` should set up the new VM from scratch for you.


- Reload the Vagrant box to make sure it's updated.

    ```bash
    $ cd ~/teracy-dev
    $ vagrant reload --provision
    ```

- After finishing running (take a long time to set everything up for the first time), you should
  see the following similar output:

    ```bash
    ==> default: Chef Client finished, 11/46 resources updated in 46 seconds
    ==> default: Running provisioner: save_mac_address (shell)...
        default: Running: /var/folders/59/znjnt7bn73d7c7_4l0fsdzm80000gn/T/vagrant-shell20170909-22045-ugdc8c.sh
    ==> default: Running provisioner: ip (shell)...
        default: Running: /var/folders/59/znjnt7bn73d7c7_4l0fsdzm80000gn/T/vagrant-shell20170909-22045-hbl0w8.sh
    ==> default: ip address: 192.168.0.10
    ==> default: vagrant-gatling-rsync is starting the sync engine because you have at least one rsync folder. To disable this behavior, set `config.gatling.rsync_on_startup = false` in your Vagrantfile.
    ==> default: Doing an initial rsync...
    ==> default: Rsyncing folder: /Users/hoatle/teracy-dev/workspace/ => /home/vagrant/workspace
    ==> default:   - Exclude: [".vagrant/", ".git", ".idea/", "node_modules/", "bower_components/", ".npm/", ".#*"]
    ==> default: Watching: /Users/hoatle/teracy-dev/workspace
    ```


## How to develop

- `$ docker-compose up` will check code style and run tests with default Python image.

There are environment variables to run and check with different versions of Python:

- `DEV_IMAGE`: the Python image to be used, default: "python:3.6"
- `FLASK`: the flask version to be installed, default: "0.12.2"
- `CHECK_STYLE`: `yes` or `1` to check code styles, default: "yes"
- `RUN_TEST`: `yes` or `1` to run tests, default: "yes"

For example:

```
$ vagrant ssh
$ ws
$ cd flask-classful
$ docker-compose run --rm dev
```

```
$ DEV_IMAGE=python:3.5 FLASK=0.11.0 CHECK_STYLE=no docker-compose run --rm dev
```

## How to work with docs

- Make sure the ``/etc/hosts`` file get updated automatically with the following commands:

    ```bash
    $ cd ~/teracy-dev
    $ vagrant hostmanager
    ```

- `$ ping dev.flask-classful-docs.teracy.dev` to make sure it pings to the right IP address of the VM:
   http://dev.teracy.org/docs/basic_usage.html#ip-address

- `$ cat /etc/hosts` file from the host machine to make sure there are no duplicated entries for
  `teracy-dev` or the VM IP address.

- SSH into the VM to make sure the docs app is ready by checking the docker logs output:

    ```bash
    $ vagrant ssh
    $ ws
    $ cd flask-classful/docs
    $ docker-compose logs -f
    ```

- Or you can use this shorthand command:

    ```bash
    $ vagrant ssh -c "cd workspace/flask-classful/docs && docker-compose logs -f"
    ```

- Wait for the logs running until you see the following similar output:

    ```bash
    app-dev_1    |   Running setup.py bdist_wheel for watchdog: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/3c/9c/be/e82ae5a37c19baf8abe88623d1f47d2d502bed7b54d4f34740
    app-dev_1    |   Running setup.py bdist_wheel for pathtools: started
    app-dev_1    |   Running setup.py bdist_wheel for pathtools: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/60/0d/2a/ffe065d190b580be6af9a862c68ed6a8a89c1778bd5c7ba7b8
    app-dev_1    |   Running setup.py bdist_wheel for PyYAML: started
    app-dev_1    |   Running setup.py bdist_wheel for PyYAML: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/2c/f7/79/13f3a12cd723892437c0cfbde1230ab4d82947ff7b3839a4fc
    app-dev_1    |   Running setup.py bdist_wheel for port-for: started
    app-dev_1    |   Running setup.py bdist_wheel for port-for: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/59/4e/68/d3a42868015e73913b1da097bf0cacfbd9b2261dc7f5796eda
    app-dev_1    |   Running setup.py bdist_wheel for MarkupSafe: started
    app-dev_1    |   Running setup.py bdist_wheel for MarkupSafe: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/88/a7/30/e39a54a87bcbe25308fa3ca64e8ddc75d9b3e5afa21ee32d57
    app-dev_1    |   Running setup.py bdist_wheel for itsdangerous: started
    app-dev_1    |   Running setup.py bdist_wheel for itsdangerous: finished with status 'done'
    app-dev_1    |   Stored in directory: /root/.cache/pip/wheels/fc/a8/66/24d655233c757e178d45dea2de22a04c6d92766abfb741129a
    app-dev_1    | Successfully built sphinx-autobuild tornado watchdog pathtools PyYAML port-for MarkupSafe itsdangerous
    app-dev_1    | Installing collected packages: chardet, urllib3, certifi, idna, requests, MarkupSafe, Jinja2, docutils, six, sphinxcontrib-websupport, imagesize, pytz, babel, snowballstemmer, alabaster, Pygments, Sphinx, itsdangerous, Werkzeug, click, Flask, flask-classful, PyYAML, argh, pathtools, watchdog, tornado, port-for, livereload, sphinx-autobuild
    app-dev_1    |   Running setup.py install for livereload: started
    app-dev_1    |     Running setup.py install for livereload: finished with status 'done'
    app-dev_1    | Successfully installed Flask-0.12.2 Jinja2-2.9.6 MarkupSafe-1.0 PyYAML-3.12 Pygments-2.2.0 Sphinx-1.6.3 Werkzeug-0.12.2 alabaster-0.7.10 argh-0.26.2 babel-2.5.1 certifi-2017.7.27.1 chardet-3.0.4 click-6.7 docutils-0.14 flask-classful-0.13.1 idna-2.6 imagesize-0.7.1 itsdangerous-0.24 livereload-2.5.1 pathtools-0.1.2 port-for-0.3.1 pytz-2017.2 requests-2.18.4 six-1.11.0 snowballstemmer-1.2.1 sphinx-autobuild-0.7.1 sphinxcontrib-websupport-1.0.1 tornado-4.5.2 urllib3-1.22 watchdog-0.8.3
    app-dev_1    | sphinx-autobuild -b html -d _build/doctrees   . _build/html -H 0.0.0.0 -p 80
    ```


Then open:

- http://dev.flask-classful-docs.teracy.dev or https://dev.flask-classful-docs.teracy.dev to check out
  the docs within your host machine.

- http://dev.flask-classful-docs.<vm_ip>.xip.io to check out the docs within your LAN network.

- http://ngrok-dev.flask-classful-docs.teracy.dev to check out the docs on the Internet.


### Local dev mode docs

```bash
$ vagrant ssh
$ ws
$ cd flask-classful/docs
$ docker-compose up -d && docker-compose logs -f
```

Open http://dev.flask-classful-docs.teracy.dev and edit docs files, it should auto reload when new
changes are detected.


### Local prod mode docs

```bash
$ vagrant ssh
$ ws
$ cd flask-classful/docs
$ docker-compose -f docker-compose.prod.yml build
$ docker-compose -f docker-compose.prod.yml up
```


Then open:

- http://flask-classful-docs.teracy.dev or https://flask-classful-docs.teracy.dev to check out
  the docs within your host machine.

- http://flask-classful-docs.<vm_ip>.xip.io to check out the docs within your LAN network.

- http://ngrok-prod.flask-classful-docs.teracy.dev to check out the docs on the Internet.


### Local review mode docs

To review work and PRs submitted by others, for example, with
`hoatle/flask-classful-docs:improvements-176-update-something` Docker image, run it:


```bash
$ vagrant ssh
$ ws
$ cd flask-classful/docs
$ APP_REVIEW_IMAGE=hoatle/flask-classful-docs:improvements-176-update-something docker-compose -f docker-compose.review.yml up
```


Then open:

- http://review.flask-classful-docs.teracy.dev or https://review.flask-classful-docs.teracy.dev to
  check out the docs within your host machine.

- http://review.flask-classful-docs.<vm_ip>.xip.io to check out the docs within your LAN network.

- http://ngrok-review.flask-classful-docs.teracy.dev to check out the docs on the Internet.


## travis-ci configuration

//TODO(hoatle): support this on the travis.yml file

You just need to configure travis-ci only one time. After each travis-ci build, new Docker images
are pushed, we can review your work (PRs) by running the Docker images instead of fetching git code
and build it on the local machine ourselves.

Here are things you need to do:

- Register your account at https://hub.docker.com
- Register your account at travis-ci.org
- Enable flask-classful repository on travis-ci (for example: https://travis-ci.org/hoatle/flask-classful)
- Fill in the following environment variables settings for flask-classful travis-ci project by
  following: https://docs.travis-ci.com/user/environment-variables/#Defining-Variables-in-Repository-Settings.
  In the *Name* and *Value* fields, please add the info below correlatively: 

  + Fill in "DOCKER_USERNAME" into the *Name* field and your Docker username into the *Value*  field
  + Fill in "DOCKER_PASSWORD" into the *Name* field and your Docker password into the *Value* field

And you're done!

## How to start working

- Learn how to work with teracy-dev:

  + http://dev.teracy.org/docs/basic_usage.html
  + http://dev.teracy.org/docs/advanced_usage.html

- Learn how to work with docker and docker-compose:

  + https://www.docker.com/
  + https://github.com/veggiemonk/awesome-docker

- You can use any text editor or IDE to edit the project files at `~/teracy-dev/workspace/flask-classful`.
