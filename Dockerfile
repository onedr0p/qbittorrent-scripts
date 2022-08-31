FROM python:3-alpine

COPY requirements.txt /app/requirements.txt

RUN \
  pip install --no-cache-dir -r /app/requirements.txt

COPY scripts/*.py /app

ENTRYPOINT [ "/usr/local/bin/python" ]

LABEL \
    org.opencontainers.image.title="qbittorrent-scripts" \
    org.opencontainers.image.source="https://github.com/onedr0p/qbittorrent-scripts"
