ARG  PYTHON_VERSION=3.6
ARG NGINX_VERSION=1.13

# building
FROM python:$PYTHON_VERSION

RUN mkdir -p /opt/app

ENV TERM=xterm APP=/opt/app

WORKDIR $APP

ADD requirements.txt $APP/

RUN pip install -r requirements.txt

ADD . $APP

RUN make html

# packaging
FROM nginx:$NGINX_VERSION

LABEL authors="hoatle <hoatle@teracy.com>"

RUN mkdir -p /opt/app

ENV TERM=xterm APP=/opt/app

WORKDIR $APP

# add more arguments from CI to the image so that `$ env` should reveal more info
ARG CI_BUILD_ID
ARG CI_BUILD_REF
ARG CI_REGISTRY_IMAGE
ARG CI_BUILD_TIME

ENV CI_BUILD_ID=$CI_BUILD_ID CI_BUILD_REF=$CI_BUILD_REF CI_REGISTRY_IMAGE=$CI_REGISTRY_IMAGE \
    CI_BUILD_TIME=$CI_BUILD_TIME

COPY --from=0 /opt/app/_build/html /usr/share/nginx/html
