// Load required packages
var sequelize = require('./db.js');
var Cinema = require('./cinema.js');
var Movie = require('./movie.js');
var DataTypes = require('sequelize');
// Define our showing schema
var Showing = sequelize.define('showing', {
  cinema_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  movie_id: {
    type: DataTypes.STRING,
    primaryKey: true
  }
});

Cinema.hasMany(Showing, {foreignKey: 'cinema_id'});
Showing.belongsTo(Cinema, {foreignKey: 'cinema_id', targetKey: 'cinema_id'});

Movie.hasMany(Showing, {foreignKey: 'movie_id'});
Showing.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});
// Export the model
module.exports = Showing;
