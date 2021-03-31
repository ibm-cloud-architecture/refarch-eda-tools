# In order to build the docker image out of this file execute:
# docker build -t "ibmcase/python-schema-registry-lab:latest" .

FROM python:3.7-stretch
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/home:/tmp/lab
RUN pip install --upgrade pip \
  && pip install --user pipenv requests black pytest numpy pandas confluent_kafka asyncio flask
# Install the following avro version due to the following bug: https://github.com/confluentinc/confluent-kafka-python/issues/610
# RUN python -mpip install --user avro-python3==1.8.2
RUN python -mpip install --user avro-python3

# Install kaf CLI (https://github.com/birdayz/kaf)
# RUN curl https://raw.githubusercontent.com/birdayz/kaf/master/godownloader.sh | BINDIR=/usr/local/bin bash
# RUN mkdir /root/.kaf
# COPY kaf-config /root/.kaf/
# RUN mv /root/.kaf/kaf-config /root/.kaf/config

# Util
RUN echo "alias ll='ls -all'" >> /root/.bashrc

# Lab files (we will be mounting these)
# COPY kafka /home/kafka
# COPY src /home/src
# COPY avro_files /home/avro_files


