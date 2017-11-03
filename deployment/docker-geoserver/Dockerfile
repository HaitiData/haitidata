FROM tomcat:9-jre8
MAINTAINER GeoNode Development Team

#
# Set GeoServer version and data directory
#
ENV GEOSERVER_VERSION=2.10.x
ENV GEOSERVER_DATA_DIR="/geoserver_data/data"
ENV GEOWEBCACHE_CACHE_DIR="/geowebcache"

RUN mkdir -p $GEOSERVER_DATA_DIR
ADD compiled_geoserver_data /geoserver_data/data

ADD resources /tmp/resources

# Custom settings for envronment variables
ENV GEOSERVER_OPTS "-Djava.awt.headless=true -server -Xms16G -Xmx32G -Xrs -XX:PerfDataSamplingInterval=500 \
 -Dorg.geotools.referencing.forceXY=true -XX:SoftRefLRUPolicyMSPerMB=36000 -XX:+UseParallelGC -XX:NewRatio=2 \
 -XX:+CMSClassUnloadingEnabled"

#-XX:+UseConcMarkSweepGC use this rather than parallel GC?
ENV JAVA_OPTS "$JAVA_OPTS $GEOSERVER_OPTS "

#
# Download and install GeoServer
#
RUN if [ ! -f /tmp/resources/geoserver.war ]; then \
    wget --progress=bar:force:noscroll http://build.geonode.org/geoserver/latest/geoserver-${GEOSERVER_VERSION}.war \
      -O /tmp/resources/geoserver.war; \
    fi; \

    unzip /tmp/resources/geoserver.war -d $CATALINA_HOME/webapps/geoserver \
    && rm -rf $CATALINA_HOME/webapps/geoserver/data \
    && rm -rf /tmp/geoserver


# copy the script and perform the run of scripts from entrypoint.sh
RUN mkdir -p /usr/local/tomcat/tmp
WORKDIR /usr/local/tomcat/tmp

RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y python python-pip python-dev \
    && pip install --upgrade pip

COPY entrypoint.sh /usr/local/tomcat/tmp

RUN chmod +x /usr/local/tomcat/tmp/entrypoint.sh

ADD broker.xml /tmp/broker.xml

# Install any plugin zip files in resources/plugins
RUN if ls /tmp/resources/plugins/*.zip > /dev/null 2>&1; then \
      for p in /tmp/resources/plugins/*.zip; do \
        unzip $p -d /tmp/gs_plugin \
        && mv /tmp/gs_plugin/*.jar $CATALINA_HOME/webapps/geoserver/WEB-INF/lib/ \
        && rm -rf /tmp/gs_plugin; \
      done; \
    fi

COPY tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml
COPY context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml

ENV activemq.transportConnectors.server.uri="tcp://0.0.0.0:0?maximumConnections=1000&wireFormat.maxFrameSize=104857600&jms.useAsyncSend=true&transport.daemon=true&trace=true"
ENV activemq.base="$CLUSTER_CONFIG_DIR/tmp"

CMD ["/usr/local/tomcat/tmp/entrypoint.sh"]
