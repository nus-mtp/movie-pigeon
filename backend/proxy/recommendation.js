var recommendation = require('../models/recommendation');
var movie = require('../models/movie');
var bookmarks = require('../models/bookmarks.js');
var publicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');

module.exports.getAllRecommendation = function (userId) {
  return movie.findAll({
    include: [
      {
        model: publicRate,
        include: [
          RatingSource
        ]
      },
      {
        model: bookmarks,
        where: {
          user_id: userId
        },
        required: false
      },
      {
        model: UserRating,
        where: {
          user_id: userId
        },
        required: false
      },
      {
        model: recommendation,
        where: {
          user_id: userId
        },
        required: true
      }
    ]
  })
};
