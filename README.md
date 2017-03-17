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
