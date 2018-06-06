FROM gliderlabs/alpine:3.6
MAINTAINER Simon Egersand "s.egersand@gmail.com"

RUN apk add --update --no-cache \
    py-pip \
    python3 \
    python2-dev \
    python3-dev \
    build-base \
    linux-headers \
    curl

ADD requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -qr /tmp/requirements.txt

ADD src /src
ADD app.py /app.py
ADD images /images
ADD static /static
ADD templates /templates

WORKDIR /

# Expose is not supported by Heroku
# EXPOSE 8000

# Run server as non-root user
RUN adduser -D nonroot
USER nonroot

# $PORT is set by Heroku
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT app:app
