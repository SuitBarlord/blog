FROM python:3.10

WORKDIR /blog
COPY . /blog/

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000

