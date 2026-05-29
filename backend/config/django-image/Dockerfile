FROM python:3.12-bookworm

RUN apt-get update && apt-get install python3-dev libgdal-dev graphviz-dev -y --force-yes

WORKDIR /usr/src/app

RUN pip install --upgrade pip && pip install --upgrade setuptools

COPY requeriments.txt ./

RUN pip install --no-cache-dir -r requeriments.txt

EXPOSE 8000

RUN mkdir /scripts
COPY django-image/runserver.sh /scripts/
RUN chmod +x /scripts -R

CMD ["/scripts/runserver.sh"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]