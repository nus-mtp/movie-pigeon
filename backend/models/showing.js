// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
var Cinema = require('./cinema.js');
var Movie = require('./movie.js');
// Define our cinema schema
var Showing = sequelize.define('showing', {
});

Cinema.belongsToMany(Movie, {
  through: Showing,
  foreignKey: 'cinema_id'
});
Movie.belongsToMany(Cinema, {
  through: Showing,
  foreignKey: 'movie_id'
});


// Export the model
module.exports = Showing;
