#!/usr/bin/env bash
IMAGE_NAME=haitidata_django
TAG_NAME=1.0
docker build -t dimasciput/${IMAGE_NAME} .
docker tag dimasciput/${IMAGE_NAME}:latest dimasciput/${IMAGE_NAME}:${TAG_NAME}
docker push dimasciput/${IMAGE_NAME}:${TAG_NAME}