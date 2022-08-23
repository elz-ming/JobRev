# ========== FROM PYTHON ========== #

FROM python:3.9

# install cron (cron)
RUN apt update
RUN apt-get install cron -y
RUN alias py=python

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# working directort
WORKDIR /usr/src/app


COPY ./app .
COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# running migrations
RUN python manage.py migrate

# django-crontab logfile (cron)
RUN mkdir /cron
RUN touch /cron/django_cron.log

# expose (cron)
EXPOSE 8000

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi", "service cron start", "python manage.py runserver 0.0.0.0:8000"]