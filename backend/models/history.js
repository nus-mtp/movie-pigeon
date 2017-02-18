// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
var User = require('./user.js');
var Movie = require('./movie.js');
// Define our history schema
var history = sequelize.define('user_ratings', {
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

User.hasMany(history, {foreignKey: 'user_id'});
history.belongsTo(User, {foreignKey: 'user_id', targetKey: 'id'});

Movie.hasMany(history, {foreignKey: 'movie_id'});
history.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});
// Export the model
module.exports = history;
