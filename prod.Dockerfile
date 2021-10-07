FROM python:3.7.5-slim-stretch

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install wait-for-it
COPY . ./

RUN python manage.py collectstatic --noinput

RUN adduser myuser
USER myuser

CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT