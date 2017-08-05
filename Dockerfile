FROM python:3.5

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /
RUN ./manage.py migrate

EXPOSE 8000

CMD ["uwsgi", "--ini=etc/uwsgi.ini"]
