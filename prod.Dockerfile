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
RUN chmod 755 ./run_prod.sh
RUN chown -R myuser:myuser ./run_prod.sh

USER myuser

CMD wait-for-it -t 15 -s $DATABASE_URL -- ./run_prod.sh
