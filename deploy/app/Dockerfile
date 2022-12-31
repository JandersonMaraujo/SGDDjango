FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /srv/app

WORKDIR /srv/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT [ "sh", "./deploy/app/entrypoint.sh" ]
# ["python", "manage.py", "runserver", "0.0.0.0:5001"]
