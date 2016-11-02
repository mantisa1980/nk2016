# dockerfile of image:nk2016_web:001
FROM ubuntu:14.04
MAINTAINER duyhsieh from mantisa1980@gmail.com
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential python
RUN pip install gunicorn gevent falcon pymongo==2.8 redis requests
RUN apt-get clean
#CMD ["/usr/bin/mongod", "--config", "/etc/mongodb.conf"]
#CMD ["/bin/bash"]
