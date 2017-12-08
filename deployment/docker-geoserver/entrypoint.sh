#!/bin/bash
set -e

source /root/.bashrc

echo "Setting cluster dir..."
randomString=$(openssl rand -hex 8)
export CLUSTER_CONFIG_DIR="${GEOSERVER_DATA_DIR}/cluster/instance_$randomString"

echo "Remove redundant library..."
[ -e /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/bcprov-jdk14-138.jar ] && rm /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/bcprov-jdk14-138.jar

echo "Cleaning old cluster settings ..."
rm -vf $CLUSTER_CONFIG_DIR/*

export CATALINA_OPTS=''

# start tomcat
exec catalina.sh run
