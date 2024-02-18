# Base build
FROM python:3.11-alpine as base
RUN apk add --update --virtual .build-deps \
    build-base \
    python3-dev
#    postgresql-dev \
#    libpq

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Now multistage build
FROM python:3.11-alpine
#RUN apk add libpq
COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERRED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV TZ=Africa/Tunis
