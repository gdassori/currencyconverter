FROM python:3.6.8-slim-stretch

RUN mkdir /app
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /root/.cache
RUN rm -rf /tmp/requirements.txt

COPY ./ /app
COPY LICENSE /app

WORKDIR "/app"

CMD ["python", "-m", "src.app"]