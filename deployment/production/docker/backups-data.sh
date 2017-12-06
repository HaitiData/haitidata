#!/bin/bash

mediadir="./media"
staticdir="./static"

echo "Create media directory if not already exist"
[ -d $mediadir ] || mkdir $mediadir

echo "Copy media data from django container"
sudo cp -a /var/lib/docker/volumes/django-media-data/_data/. $mediadir

echo "Create static directory if not already exist"
[ -d $staticdir ] || mkdir $staticdir

echo "Copy static data from django container"
sudo cp -a /var/lib/docker/volumes/django-static-data/_data/. $staticdir
