#!/bin/sh
docker create -v ~/nk2016:/hostdata --name nk2016_hostdata ubuntu
docker create -v ~/nk2016/dbdata:/data/db --name nk2016_dbdata ubuntu
#docker run -d -ti --name nk2016_mongo mongo
docker run -d -ti --name nk2016_mongo --volumes-from nk2016_dbdata mongo
docker run -d -t --name nk2016_webserver -p 8888:8888 --volumes-from nk2016_hostdata --link nk2016_mongo:mongo mantisa1980/nk2016_webserver
