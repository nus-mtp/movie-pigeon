var recommendation = require('../models/recommendation');
var movie = require('../models/movie');
var bookmarks = require('../models/bookmarks.js');
var publicRate = require('../models/PublicRate.js');
var ratingSource = require('../models/ratingSource.js');
var userRating = require('../models/history.js');
var showing  = require('../models/showing');

module.exports.getAllRecommendation = function (userId) {
  return movie.findAll({
    include: [
      {
        model: publicRate,
        include: [
          ratingSource
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
        model: userRating,
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
      },
      {
        model: showing,
        required: false
      }
    ]
  })
};
