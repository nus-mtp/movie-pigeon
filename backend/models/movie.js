// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
// Define our movie schema
var Movie = sequelize.define('movies', {
  movie_id: {
    type: DataTypes.STRING,
    allowNull: false,
    primaryKey: true
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  production_year: {
    type: DataTypes.INTEGER
  },
  rated: {
    type: DataTypes.STRING
  },
  plot: {
    type: DataTypes.TEXT
  },
  actors: {
    type: DataTypes.TEXT
  },
  language: {
    type: DataTypes.STRING
  },
  country: {
    type: DataTypes.STRING
  },
  genre: {
    type: DataTypes.STRING
  },
  poster_url: {
    type: DataTypes.TEXT
  },
  released: {
    type: DataTypes.DATE
  },
  runtime: {
    type: DataTypes.STRING
  },
  director: {
    type: DataTypes.STRING
  },
  type: {
    type: DataTypes.STRING
  }
});

sequelize.sync({});
// Export the model
module.exports = Movie;
