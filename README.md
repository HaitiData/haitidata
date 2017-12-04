# Haitidata

You should write some docs, it's good for the soul.

# Docker installation

## Install docker
Follow the instructions from:
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

## Install docker-compose
Follow the instructions from:
https://docs.docker.com/compose/install/#install-compose

## Get project code
Clone the repo:
```
git clone https://github.com/HaitiData/haitidata.git
```

## Run project
Run the docker container:
```
cd deployment
make deploy
make update-migrations-localization
```

then you can visit http://0.0.0.0:33300
