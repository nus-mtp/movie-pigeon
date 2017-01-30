// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
// Define our token schema
var Movie = sequelize.define('movies', {
  id: {
    type: DataTypes.STRING,
    allowNull: false,
    primaryKey: true
  },
  title: {
    type: DataTypes.STRING,
    allowNull: false
  },
  productionYear: {
    type: DataTypes.STRING
  },
  Rated: {
    type: DataTypes.STRING
  },
  Plot: {
    type: DataTypes.STRING
  },
  Actors: {
    type: DataTypes.ARRAY(DataTypes.STRING)
  },
  Lanugage: {
    type: DataTypes.STRING
  },
  Country: {
    type: DataTypes.STRING
  },
  runtime: {
    type: DataTypes.STRING
  },
  PosterUrl: {
    type: DataTypes.STRING
  }
});

sequelize.sync({});

// Export the Mongoose model
module.exports = Movie;
