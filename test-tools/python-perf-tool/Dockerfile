FROM python:3.7-stretch
ENV PATH=/root/.local/bin:$PATH
RUN pip install --upgrade pip \
  && pip install --user pipenv requests confluent-kafka flask 
ENV PYTHONPATH=/home/perf-tests
WORKDIR /home
EXPOSE 5000
CMD bash

