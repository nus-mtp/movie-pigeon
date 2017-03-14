var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');
var Bookmark = require('../models/bookmarks.js');
var PublicRate = require('../models/PublicRate.js');
var Movie = require('../models/movie.js');
var Showing = require('../models/showing.js');

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

module.exports.getAllShowingMovie = function (userId) {
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
        attributes: [],
        required: true
      }
    ]
  });
};

module.exports.getShowingByCinema = getShowingByCinema;
