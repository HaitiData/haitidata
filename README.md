# Haitidata

Basic commands for setting up HaitiData from scratch on Ubuntu 16.04

# Update apt repository
```
sudo apt update
```

# Install curl and git
```
sudo apt install curl git
```

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
make fresh-deploy
make update-migrations-localization
make upload-fixtures
make collectstatic
```

then you can visit http://0.0.0.0:33300```
