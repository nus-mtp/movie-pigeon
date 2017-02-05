// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
var RatingSource = require('./ratingSource.js');
var Movie = require('./movie.js');
// Define our public_rate schema
var Rates = sequelize.define('public_ratings', {
  vote: {
    type: DataTypes.INTEGER
  },
  score: {
    type: Datatypes.FLOAT
  }
});

RatingSource.belongsToMany(Movie, {
  through: Rates,
  foreignKey: 'source_id'
});
Movie.belongsToMany(RatingSource, {
  through: Rates,
  foreignKey: 'movie_id'
});

sequelize.sync({});
// Export the model
module.exports = Rates;
