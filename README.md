[![Build
Status](https://travis-ci.org/nus-mtp/movie-pigeon.svg?branch=master)](https://travis-ci.org/nus-mtp/movie-pigeon)
[![Test
Coverage](https://codeclimate.com/github/nus-mtp/movie-pigeon/badges/coverage.svg)](https://codeclimate.com/github/nus-mtp/movie-pigeon/coverage)
[![Code
Climate](https://codeclimate.com/github/nus-mtp/movie-pigeon/badges/gpa.svg)](https://codeclimate.com/github/nus-mtp/movie-pigeon)

# Movie Pigeon

Backend REST server using Nodejs, Expressjs and PostgreSQL

## Getting Started

Clone Repo

````
git clone https://github.com/nus-mtp/movie-pigeon-server.git
````

Npm install dependencies

````
cd backend & npm install
````

Start PostgreSQL and create database

````
CREATE DATABASE test
USE test
````

Generate tables using Sequelize.
You need to ensure environment variable `NODE_ENV=test`
````
cd backend/models
node sync.js
````

Start Server

````
cd backend & npm start
````

Run Tests

````
cd backend & npm test
````


# Copyright & License

Copyright (c) 2017 MoviePigeon - Released under the [MIT license](LICENSE).
