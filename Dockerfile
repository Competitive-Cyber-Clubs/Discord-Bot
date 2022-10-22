FROM python:3.10-bullseye-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY requirements.txt /tmp/pip-tmp/

RUN pip --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt  \
    && rm -rf /tmp/pip-tmp

RUN rm -rf /var/lib/apt/lists/* \
    && apt purge build-essential libpq-dev -y \
    && apt autoremove -y && pip cache purge

COPY bot /usr/src/app/bot/

WORKDIR /usr/src/app

ENV PYTHONPATH=:/usr/src/app/bot

ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "bot/main.py"]