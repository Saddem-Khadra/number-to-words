FROM python:3.11-alpine
ENV PYTHONUNBUFFERRED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV TZ=Africa/Tunis
WORKDIR /app
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
COPY . /app
