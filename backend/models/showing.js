// Load required packages
var sequelize = require('./db.js');
var Cinema = require('./cinema.js');
var Movie = require('./movie.js');
var DataTypes = require('sequelize');
var PublicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');
var Bookmark = require('../models/bookmarks.js');
// Define our showing schema
var Showing = sequelize.define('showings', {
  cinema_id: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  movie_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  type: {
    type: DataTypes.STRING
  },
  schedule: {
    type: DataTypes.DATE
  }
});

Cinema.hasMany(Showing, {foreignKey: 'cinema_id'});
Showing.belongsTo(Cinema, {foreignKey: 'cinema_id', targetKey: 'cinema_id'});

Movie.hasMany(Showing, {foreignKey: 'movie_id'});
Showing.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});

module.exports = Showing;

var getShowingByCinema = function (userId, cinemaId) {
  return Movie.findAll({
    include: [
      {
        model: PublicRate,
        include: [
          RatingSource
        ]
      },
      {
        model: UserRating,
        where: {
          user_id: userId
        },
        required: false
      },
      {
        model: Bookmark,
        where: {
          user_id: userId
        },
        required: false
      },
      {
        model: Showing,
        where: {
          cinema_id: cinemaId
        },
        required: true
      }
    ]
  });
};


module.exports.getShowingByCinema = getShowingByCinema;
