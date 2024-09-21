FROM python:3.10-alpine
ENV USER=goat
LABEL org.opencontainers.image.source=https://github.com/atonomic/scrapegoat
LABEL org.opencontainers.image.description="ScrapeGoat"
LABEL org.opencontainers.image.licenses=Apache

RUN apk update && apk add --no-cache \
    bash \
    build-base \
    chromium \
    libffi-dev \
    shadow \
    tcl \
    tk \
    ttf-dejavu \
    wget \
    xvfb \
    && apk add --no-cache --virtual .build-deps gcc musl-dev python3-tkinter \
    && pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt && \
    useradd -m -s /bin/bash "$USER"  && \
    chown -R "$USER":"$USER" /app

USER "$USER"

ENV DISPLAY=:99

CMD ["sh", "-c", "mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix && Xvfb :99 -screen 0 1024x768x16 & python3 main.py"]
