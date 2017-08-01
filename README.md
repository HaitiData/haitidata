# Haitidata

You should write some docs, it's good for the soul.

# Docker installation

## Install docker
This will install an Haitidata container

Makes sure to have docker-compose installed
```
sudo apt-get install python-pip
sudo pip install docker-compose
```

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
make update-migrations-localization:
```

then you can visit http://0.0.0.0:33300```
