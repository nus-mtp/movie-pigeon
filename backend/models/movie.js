// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
// Define our token schema
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
    type: DataTypes.STRING
  },
  rated: {
    type: DataTypes.STRING
  },
  plot: {
    type: DataTypes.STRING
  },
  actors: {
    type: DataTypes.STRING
  },
  lanugage: {
    type: DataTypes.STRING
  },
  country: {
    type: DataTypes.STRING
  },
  genre: {
    type: DataTypes.STRING
  },
  poster_url: {
    type: DataTypes.STRING
  },
  released: {
    type: DataTypes.STRING
  },
  runtime: {
    type: DataTypes.STRING
  },
  director: {
    type: DataTypes.STRING
  }
});

// Export the Mongoose model
module.exports = Movie;
