FROM python:3.9-alpine
LABEL author="Richard OBrien"

# Run Python in unbuffered mode so that outputs are not buffered 
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt

RUN mkdir /cryptomarketcap
WORKDIR /cryptomarketcap
COPY ./cryptomarketcap /cryptomarketcap

# Create user that will be used to run application only
RUN adduser -D user
USER user

