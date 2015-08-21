sphinx-deployment
=================

Automatic setup and deployment for [sphinx][] docs.

This project is intended to be used to deploy [sphinx][] project on:

- [Github Pages](https://help.github.com/categories/20/articles)
- [Rsync](http://en.wikipedia.org/wiki/Rsync)
- PaaS services: [heroku](http://heroku.com/), etc.

Usage
-----

**1. `$ make generate`**

For generating contents, alias for `$ make html`

**2. `$ make deploy`**

For short-cut deployment, it could be `$ make deploy_gh_pages`, `$ make deploy_rsync` or
`$ make deploy_heroku` basing on the configuration of `DEPLOY_DEFAULT`.

**3. `$ make gen_deploy`**

For short-cut generation and deployment: `$ make generate` and then `$ make deploy`.

**4. `$ make setup_gh_pages`**

For the first time only to create `$(DEPLOY_DIR)` to track `$(DEPLOY_BRANCH)`. This is used for
github pages deployment.

**5. `$ make setup_heroku`**

For the first time only to create `$(DEPLOY_DIR_HEROKU` to track the Heroku repo's master branch.
This is used for heroku deployment.

**6. `$ make deploy_gh_pages`**

For deploying with github pages only.

**7. `$ make deploy_rsync`**

For deploying with rsync only.

**8. `$ make deploy_heroku`**

For deploying with heroku only.


Installation
------------

**1. Bash script**

Just run this bash script from your root git repository project and it's enough.

You need to specify the `<docs_path>` to your sphinx docs directory:

``` bash
$ cd <your_project>
$ wget https://raw.githubusercontent.com/teracyhq/sphinx-deployment/develop/scripts/spxd.sh && chmod +x ./spxd.sh && ./spxd.sh -p <docs_path>
```

For example:

``` bash
$ cd my_project
$ wget https://raw.githubusercontent.com/teracyhq/sphinx-deployment/develop/scripts/spxd.sh && chmod +x ./spxd.sh && ./spxd.sh -p ./docs
```

**2. Manual**

a. You need to copy these following files to your [sphinx][] directory:

- `docs/requirements`
- `docs/sphinx_deployment.mk`
- `docs/rsync_exclude`
- `docs/.deploy_heroku/*`
- `docs/.gitignore`

b. Include `sphinx_deployment.mk` to your `Makefile`:

- Add the content below to your `Makefile`:

```
include sphinx_deployment.mk
```

- Or do with commands on terminal:

``` bash
echo '' >> Makefile
echo 'include sphinx_deployment.mk' >> Makefile
```


c.. To build with `travis-ci`, you need to copy these following files to your root project directory:

- `.travis.yml`
- `.travis/setup.sh`


Configuration
-------------

You need to configure these following deployment configurations following your project settings on
`sphinx_deployment.mk` file.

``` Makefile
# Deployment configurations from sphinx_deployment project

# default deployment when $ make deploy
# deploy_gh_pages                            : to $ make deploy_gh_pages
# deploy_rsync                               : to $ make deploy_rsync
# deploy_heroku                              : to $ make deploy_heroku
# deploy_gh_pages deploy_rsync deploy_heroku : to $ make deploy_gh_pages then $ make deploy_rsync
#                                              and then $ make deploy_heroku
# default value: deploy_gh_pages
ifndef DEPLOY_DEFAULT
DEPLOY_DEFAULT = deploy_gh_pages
endif

# The deployment directory to be deployed
ifndef DEPLOY_DIR
DEPLOY_DIR      = _deploy
endif

# The heroku deployment directory to be deployed
# we must create this separated dir to avoid any conflict with _deploy (rsync and gh_pages)
ifndef DEPLOY_DIR_HEROKU
DEPLOY_DIR_HEROKU = _deploy_heroku
endif

# Copy contents from $(BUILDDIR) to $(DEPLOY_DIR)/$(DEPLOY_HTML_DIR) directory
ifndef DEPLOY_HTML_DIR
DEPLOY_HTML_DIR = docs
endif


## -- Rsync Deploy config -- ##
# Be sure your public key is listed in your server's ~/.ssh/authorized_keys file
ifndef SSH_USER
SSH_USER       = user@domain.com
endif

ifndef SSH_PORT
SSH_PORT       = 22
endif

ifndef DOCUMENT_ROOT
DOCUMENT_ROOT  = ~/website.com/
endif

#If you choose to delete on sync, rsync will create a 1:1 match
ifndef RSYNC_DELETE
RSYNC_DELETE   = false
endif

# Any extra arguments to pass to rsync
ifndef RSYNC_ARGS
RSYNC_ARGS     =
endif

## -- Github Pages Deploy config -- ##

# Configure the right deployment branch
ifndef DEPLOY_BRANCH_GITHUB
DEPLOY_BRANCH_GITHUB = gh-pages
endif

#if REPO_URL_GITHUB was NOT defined by travis-ci
ifndef REPO_URL_GITHUB
# Configure your right github project repo
# REPO_URL       = git@github.com:teracy-official/sphinx-deployment.git
endif

## -- Heroku Deployment Config -- ##

ifndef REPO_URL_HEROKU
# Configure your right heroku repo
# REPO_URL_HEROKU = git@heroku.com:spxd.git
endif


## end deployment configuration, don't edit anything below this line ##
#######################################################################
```

Continuous Integration Build
----------------------------

**1. `travis-ci`**

Move `.travis.yml` file to your root repository project, and configure it following its
instruction there. There is a supported `.travis/setup.sh` to export variables for `Makefile`
depending on the being-built branch.

To configure secure token for `travis-ci`, please read the similar step described at
http://blog.teracy.com/2013/08/03/how-to-start-blogging-easily-with-octopress-and-teracy-dev/


**2. `jenkins`**

//TODO


Authors and contributors
------------------------

- Hoat Le: http://github.com/hoatle

- Many thanks to http://octopress.org/docs/deploying/ for inspiration.

License
-------

BSD License

```
Copyright (c) Teracy, Inc. and individual contributors.
All rights reserved.

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

```

[sphinx]: http://sphinx-doc.org
