# flask-classful dev-setup

Please follow this getting started guide to set up the development environment.

Please take a cup of coffee with you, you mostly don't have to do anything but wait for the result, enjoy!


## Setting up from scratch

### Setting up teracy-dev

- Please follow document at https://github.com/teracyhq/dev-setup/blob/develop/README.md to set up teracy-dev and dev-setup, then come back here to setting up the flask-clasful project.


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

- `$ docker-compose up` will check code style and run tests with defaul Python image.

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

## How to start working

- Learn how to work with teracy-dev:

  + http://dev.teracy.org/docs/basic_usage.html
  + http://dev.teracy.org/docs/advanced_usage.html

- Learn how to work with docker and docker-compose:

  + https://www.docker.com/
  + https://github.com/veggiemonk/awesome-docker

- You can use any text editor or IDE to edit the project files at `~/teracy-dev/workspace/flask-classful`.
