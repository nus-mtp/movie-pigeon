var rate = require('../models/history');
var movie = require('../models/movie.js');
var PublicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var Bookmark = require('../models/bookmarks.js');

module.exports.postRates = function (score, movieId, userId) {
  return rate.create({
    score: score,
    movie_id: movieId,
    user_id: userId
  })
};

module.exports.getAllRates = function (userId) {
  return movie.findAll({
    include: [
      {
        model: PublicRate,
        include: [
          RatingSource
        ]
      },
      {
        model: rate,
        where: {
          user_id: userId
        },
        required: true
      },
      {
        model: Bookmark,
        where: {
          user_id: userId
        },
        required: false
      }
    ]
  })
};

module.exports.getSpecificRate = function (userId, movieId) {
  return rate.find({
    where: {
      movie_id: movieId,
      user_id: userId
    }
  })
};

module.exports.updateRates = function (rate, score) {
  return rate.updateAttributes({
    score: score
  })
};
