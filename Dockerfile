FROM python:3.9-alpine as builder

LABEL maintainer=<pmcfadde@thoughtworks.com>
LABEL org.opencontainers.image.source https://github.com/ThoughtWorks-DPS/lab-api-teams
ENV MUSL_LOCPATH=/usr/share/i18n/locales/musl \
    LANG="C.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

# hadolint ignore=DL3003
RUN apk add --no-cache \
        libintl==0.21-r2 && \
    apk --no-cache add --virtual build-dependencies \
        cmake==3.23.1-r0 \
        make==4.3-r0 \
        musl==1.2.3-r0 \
        musl-dev==1.2.3-r0 \
        musl-utils==1.2.3-r0 \
        gcc==11.2.1_git20220219-r2 \
        gettext-dev==0.21-r2 && \
    wget -q https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip && \
    unzip musl-locales-master.zip && cd musl-locales-master && \
    cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && \
    make && make install && \
    cd .. && rm -r musl-locales-master && \
    adduser -D teams && \
    apk del build-dependencies

USER teams
WORKDIR /home/teams

COPY --chown=teams:teams /api ./api
COPY --chown=teams:teams Pipfile Pipfile
ENV PATH="/home/teams/.local/bin:/home/teams/.venv/bin:${PATH}"

RUN pip install --user --no-cache-dir pipenv==2022.4.21 && \
    PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

CMD [".venv/bin/uvicorn", "api.main:api", "--host", "0.0.0.0", "--port", "8000"]
