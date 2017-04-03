// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
var RatingSource = require('./ratingSource.js');
var Movie = require('./movie.js');
// Define our public_rate schema
var Rates = sequelize.define('public_ratings', {
  movie_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  source_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  vote: {
    type: DataTypes.INTEGER
  },
  score: {
    type: DataTypes.FLOAT
  },
  updated_at: {
    type: DataTypes.DATE
  }
});

RatingSource.hasMany(Rates, {foreignKey: 'source_id'});
Rates.belongsTo(RatingSource, {foreignKey: 'source_id', targetKey: 'source_id'});

Movie.hasMany(Rates, {foreignKey: 'movie_id'});
Rates.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});
// Export the model
module.exports = Rates;
