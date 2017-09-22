FROM kartoza/geonode_db
MAINTAINER Kartoza

ENV POSTGRES_USER=docker
ENV POSTGRES_PASS=docker

RUN mkdir -p /fresh-backups/
COPY fresh-database.dmp /fresh-backups/fresh-database.dmp
#RUN su - postgres -c "dropdb --if-exists gis"
#RUN su - postgres -c "dropdb --if-exists geonode_data"
#RUN su - postgres -c "createdb -O docker -T template_postgis gis"
#RUN su - postgres -c "createdb -O docker -T template_postgis geonode_data"
#RUN pg_restore /fresh-backups/fresh-database.dmp | su - postgres -c "psql gis"
