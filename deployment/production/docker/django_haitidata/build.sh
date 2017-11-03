#!/usr/bin/env bash
IMAGE_NAME=haitidata_django
TAG_NAME=latest
docker build -t kartoza/${IMAGE_NAME} .
docker tag kartoza/${IMAGE_NAME}:latest kartoza/${IMAGE_NAME}:${TAG_NAME}
docker push kartoza/${IMAGE_NAME}:${TAG_NAME}