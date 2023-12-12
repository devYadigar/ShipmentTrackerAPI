FROM python:3.8
LABEL authors="yadigar"


# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y default-mysql-client && \
    apt-get install -y build-essential default-libmysqlclient-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

CMD ["/scripts/run.sh"]