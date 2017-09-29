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
RUN apt-get install software-properties-common -y

# Set the locale - change to your preferred locale ... We use South African english
# We do this as cartridge (ecommerce platform for mezzanine) relies on
# the locale to set the correct number of decimal places for the MoneyField
RUN echo "deb http://ftp.debian.org/debian jessie main" >> /etc/apt/sources.list.d/gdal.list
RUN apt-get update

#------------- Application Specific Stuff ----------------------------------------------------
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

ADD REQUIREMENTS.txt /REQUIREMENTS.txt

RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

RUN pip uninstall django-user-accounts -y
RUN pip install git+https://github.com/GeoNode/geonode-user-accounts@invite-user

# Install translation
RUN apt-get -y --force-yes install gettext

#------------- Gdal Specific Stuff ----------------------------------------------------
RUN apt-get install gdal-bin
RUN cd /home/web && wget http://download.osgeo.org/gdal/$GDAL_VERSION/gdal-$GDAL_VERSION.tar.gz && tar -xvzf gdal-$GDAL_VERSION.tar.gz && rm /home/web/gdal-$GDAL_VERSION.tar.gz
RUN cd /home/web/gdal-$GDAL_VERSION && ./configure -prefix=/usr/ && make && make install && cd /home/web/gdal-$GDAL_VERSION/swig/python && python setup.py install && rm -rf /home/web/gdal-$GDAL_VERSION

#------------- Geoserver Specific Stuff ----------------------------------------------------
RUN echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -t jessie-backports openjdk-8-jre-headless ca-certificates-java openjdk-8-jdk tomcat8 tomcat8-admin -y

ENV CATALINA_HOME /var/lib/tomcat8
ENV PATH $CATALINA_HOME/bin:$PATH
WORKDIR $CATALINA_HOME

ENV GS_VERSION 2.10.x
ENV GEOSERVER_DATA_DIR /geoserver/data_dir

ADD resources /tmp/resources

RUN apt-get install zip unzip -y
RUN cd $CATALINA_HOME
# A little logic that will fetch the geoserver war zip file if it
# is not available locally in the resources dir
RUN if [ ! -f /tmp/resources/geoserver.zip ]; then \
    wget -c http://build.geonode.org/geoserver/latest/geoserver-${GS_VERSION}.war \
      -O /tmp/resources/geoserver.war; \
    fi; \
    unzip /tmp/resources/geoserver.war -d $CATALINA_HOME/webapps/geoserver \
    && rm -rf $CATALINA_HOME/webapps/geoserver/data \
    && rm -rf /tmp/geoserver

#RUN service tomcat8 start

EXPOSE 8000
EXPOSE 8080

WORKDIR /home/web/django_project
CMD ["uwsgi", "--env", "LC_ALL=en_US.UTF-8", "--ini", "/uwsgi.conf"]
