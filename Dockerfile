FROM python:3-alpine

COPY requirements.txt /app/requirements.txt

RUN \
  pip install --no-cache-dir -r /app/requirements.txt

COPY scripts/*.py /app

ENTRYPOINT [ "/usr/local/bin/python" ]

LABEL "maintainer"="Devin Buhl <devin.kray@gmail.com>, Bernd Schorgers <me@bjw-s.dev>"
LABEL "org.opencontainers.image.source"="https://github.com/k8s-at-home/qbittorrent-scripts"
