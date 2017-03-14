var movie = require('../models/movie');
var bookmarks = require('../models/bookmarks.js');
var publicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');

module.exports.getAllBookmarks = function (userId) {
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
        required: true
      },
      {
        model: UserRating,
        where: {
          user_id: userId
        },
        required: false
      }
    ]
  })
};

module.exports.getSpecificBookmark = function (userId, movieId) {
  return bookmarks.find({
    where: {
      user_id: userId,
      movie_id: movieId
    }
  });
};

module.exports.postBookmark = function (movieId, userId) {
  return bookmarks.create({
    movie_id: movieId,
    user_id: userId
  });
};
