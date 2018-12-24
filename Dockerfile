FROM python:3.5

RUN adduser --disabled-password ubuntu

WORKDIR /home/ubuntu

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN apt-get -y update && apt-get -y install apache2 apache2-dev libapache2-mod-wsgi-py3

COPY chatterbox /var/www/chatter_app/chatterbox

RUN chmod -R 777 /var/www/chatter_app
WORKDIR /etc/apache2/sites-available
#RUN pwd
#RUN ls
COPY chatterbox.conf /etc/apache2/sites-available/chatterbox.conf

RUN a2dissite * && a2ensite chatterbox

EXPOSE 80
ENTRYPOINT apachectl -D FOREGROUND
