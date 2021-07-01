# crypto-market-cap-api
A basic Crypto Market Cap API making use of the CoinGecko API

# Environment Setup

## Docker

macOS and Windows users can install Docker Desktop which contains both Docker and Docker-Compose tools rrequired to run the project using Docker.

Linux users need to follow the instructions on [Get Docker CE](https://docs.docker.com/engine/install/ubuntu/) for Ubuntu and then Install [Docker Compose](https://docs.docker.com/compose/install/) separately.

# Running the project using Docker

The crypto-market-cap-api has been setup to make use of Docker (using a lightweight Alpine base image) so that the container can more easily be run or deployed to various environments.

1. Build the image using Docker Compose:
`docker-compose build`

2. Run Tests to make sure everything is working:
`docker-compose run --rm app sh -c "python manage.py test && flake8"`


# Running Tests and Linting


## Steps for Gently Scaling with 3rd party CoinGecko API

This project takes steps to reducing the number of calls made to the 3rd party CoinGecko API by caching the results of each call for a specific period. The period chosen should be based on the potential frequency and period between changes. 

For example: A new coin being added to the CoinGecko coins list is unlikely to happen more than a few times a day (if at all).

The cache for retrieving the list of available coins on CoinGecko is set to timeout after 12 hours for the purpose of this assignment but would ideally be analysed and adjusted accordingly. 

The Crypto Market Cap API makes use of a per view cache by caching the output of individual views. Local memory caching is used which means that each process has its own private cache instance - this cache is not particularly memory-efficient and is not recommended for production environments. 

## Project Technology

The following section outlines the technology that was used to build this project.

1. Python

The crypto-market-cap-api project is built using Pyton 3.9 following the PEP-8 style guidelines. 

2. Django

Django is the python based webframework that is used to create this api. 

3. Django REST Framework

An extension of Django that adds useful features for building REST APIs. Serializers are used to create validation on all requests to the API and to convert JSON objects to Django models. The Django REST Framework also provides a browsable API which can be used for testing and exploring the created api. 

4. Docker

A virtualisation tool that provides a mechanism for isolating project dependencies. Docker is used to wrap the crypto-market-cap-api project and its dependencies into a single image that can be run independently on any machine or server. This leads to a consistent development environment as well as a container that can be deployed to various cloud platforms.  

5. Docker Compose 

A tool that allows us to run the Docker image and easily manage the different services that make up this project. Currently there is only one service as a Database integration was not required. 

6. Travis-CI

A continuous integration tool that is used to automatically run linting and unit tests when a change is made to the project repository. 

You can view the build statuses over time using the [Travis-ci Dashboard](https://travis-ci.com/github/RichardOB/crypto-market-cap-api)