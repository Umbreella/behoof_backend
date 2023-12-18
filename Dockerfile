FROM python:3.10-slim as builder

RUN pip install poetry

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN poetry config virtualenvs.in-project true --local && \
    poetry install --without dev


FROM python:3.10-slim

RUN apt-get update
RUN apt-get -y install binutils libproj-dev gdal-bin

COPY --from=builder /usr/src/app /usr/src/app

WORKDIR /usr/src/app

EXPOSE 8000

ENV PATH="/usr/src/app/.venv/bin:$PATH"

CMD ["gunicorn", "behoof.wsgi:application", "-b", ":8000"]
