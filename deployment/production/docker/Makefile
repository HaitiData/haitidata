SHELL := /bin/bash

build-nginx:
	@cd nginx && ./build.sh

build-django:
	@cd django_haitidata && ./build.sh

build-db:
	@cd db && ./build.sh

build-geoserver:
	@cd geoserver && ./build.sh

build-all: build-db build-nginx build-django
