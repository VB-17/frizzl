FROM python:3


WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/frizzl-env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 16.13.1

RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

RUN . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH


RUN groupadd appuser && \ 
    useradd -m -d /home/appuser -s /bin/bash -g appuser -G sudo,root appuser

COPY requirements.txt .
RUN pip install pip --upgrade && pip install -r requirements.txt
COPY --chown=appuser:appuser . .

USER appuser
RUN python3 manage.py tailwind install