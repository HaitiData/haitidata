#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base
MAINTAINER Irwan Fathurrahman<irwan@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
#ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

# Pandoc needed to generate rst dumps, uic compressor needed for django-pipeline
RUN apt-get update -y

# Set the locale - change to your preferred locale ... We use South African english
# We do this as cartridge (ecommerce platform for mezzanine) relies on
# the locale to set the correct number of decimal places for the MoneyField
RUN echo "deb http://ftp.debian.org/debian jessie main" >> /etc/apt/sources.list.d/gdal.list
RUN apt-get update

#-------------Application Specific Stuff ----------------------------------------------------
ENV GDAL_VERSION 2.1.3

RUN apt-get install locales && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.UTF-8
RUN apt-get install libgdal-dev -y
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal
ENV TEST a

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN pip install uwsgi

COPY requirements-haitidata.txt /requirements-haitidata.txt
RUN pip install -r /requirements-haitidata.txt

# Install translation
RUN apt-get -y --force-yes install gettext

RUN apt-get install gdal-bin python-gdal -y
# Open port 8080 as we will be running our uwsgi socket on that

EXPOSE 8080
WORKDIR /home/web/django_project
CMD ["uwsgi", "--env", "LC_ALL=en_US.UTF-8", "--ini", "/uwsgi.conf"]
