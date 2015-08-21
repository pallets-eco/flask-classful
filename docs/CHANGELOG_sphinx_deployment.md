Change Log
==========

[0.3.0][] (2013-11-26)
----------------------

- Improvement
    + [SPXD-10] - Deploy vX.X.X tag to docs/X.X.X instead of docs/vX.X.X

- New Feature
    + [SPXD-9] - PaaS deployment: heroku

- Migration (from v0.2.0 to v0.3.0)
    + `REPO_URL` was changed to `REPO_URL_GITHUB`
    + `DEPLOY_BRANCH` was changed to `DEPLOY_BRANCH_GITHUB`
    + `$ make push` was changed to `$ make deploy_gh_pages`
    + `$ make rsync` was changed to `$ make deploy_rsync`


[0.2.0][] (2013-09-26)
----------------------

- Improvement
    + [SPXD-6] - remove duplication of git init when setup_gh_pages

- New Feature
    + [SPXD-5] - Rsync support


[0.1.0][] (2013-08-18)
----------------------

- Improvement
    + [SPXD-2] - remove "make init_gh_pages" step

- New Feature
    + [SPXD-1] - make gen_deploy
    + [SPXD-3] - installation bash script


[0.1.0]: https://issues.teracy.org/secure/ReleaseNote.jspa?version=10003&styleName=Text&projectId=10405&Create=Create&atl_token=BD5N-YNBS-EHHQ-478Z%7C87dd31199258f9de5ade180582481463461ded32%7Clin

[0.2.0]: https://issues.teracy.org/secure/ReleaseNote.jspa?projectId=10405&version=10004

[0.3.0]: https://issues.teracy.org/secure/ReleaseNote.jspa?projectId=10405&version=10301
