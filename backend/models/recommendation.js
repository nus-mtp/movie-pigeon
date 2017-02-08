// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
var User = require('./user.js');
var Movie = require('./movie.js');
// Define our recommendation schema
var Recommendation = sequelize.define('recommendations', {
  user_id: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  movie_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  score: {
    type: DataTypes.FLOAT
  }
});

User.hasMany(Recommendation, {foreignKey: 'user_id'});
Recommendation.belongsTo(User, {foreignKey: 'user_id', targetKey: 'id'});

Movie.hasMany(Recommendation, {foreignKey: 'movie_id'});
Recommendation.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});
// Export the model
module.exports = Recommendation;
