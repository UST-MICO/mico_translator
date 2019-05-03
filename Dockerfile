FROM python:3.7-slim-stretch

RUN pip install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY translator ./translator

CMD python -m translator
