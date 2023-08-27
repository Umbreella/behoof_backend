FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install binutils libproj-dev gdal-bin python3-pip

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /usr/src/app/

EXPOSE 8000

CMD ["uvicorn", "behoof.asgi:application", "--host", "0.0.0.0", "--port", "8000"]