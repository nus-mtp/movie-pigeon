var Movie = require('../models/movie.js');
var PublicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');
var Bookmark = require('../models/bookmarks.js');

exports.getMovieByTitle = function (userId, searchString, offset, limit) {
  return Movie.findAndCountAll({
    where: {
      title: {$ilike: searchString}
    },
    limit: limit,
    offset: offset,
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
      }
    ]
  })
};

module.exports.getMovieById = function (movieId) {
  return Movie.find({
    where: {
      movie_id: movieId
    }
  })
};
