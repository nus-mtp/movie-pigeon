// var recommendation = require('../proxy/recommendation');
var recommendation = require('../models/recommendation');
var movie = require('../models/movie');
var bookmarks = require('../models/bookmarks.js');
var publicRate = require('../models/PublicRate.js');
var ratingSource = require('../models/ratingSource.js');
var userRating = require('../models/history.js');
var sequelize = require('../models/db');


// Create endpoint /api/recommendations for GET
module.exports.getRecommendation = function (req, res) {
  var userId = req.user.id;

  recommendation.count({
    where: {
      user_id: userId
    }
  })
    .then(function (result) {
      if (result != 0) {
        movie.findAll({
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
            }
          ]
        })
          .then(function (recoms) {
            if (recoms) {
              res.json(recoms);
            }
          })
      } else {
        sequelize.query('SELECT m.*, ' +
          'r.vote as imdb_vote,' +
          'r.score as imdb_score, ' +
          'r1.vote as douban_vote, ' +
          'r1.score as douban_score, ' +
          'r2.vote as trakt_vote, ' +
          'r2.score as trakt_score, ' +
          'bookmarks.movie_id as bookmarks_movie_id ' +
          'FROM public_ratings r, public_ratings r1, public_ratings r2, movies m LEFT OUTER JOIN bookmarks ON m.movie_id = bookmarks.movie_id and bookmarks.user_id = '+ userId +
          ' WHERE ' +
          'r.movie_id = r1.movie_id AND r1.movie_id = r2.movie_id AND r2.movie_id = r.movie_id'+
          ' AND r.source_id = \'1\' AND r1.source_id = \'2\' AND r2.source_id = \'3\' ' +
          'AND r.movie_id = m.movie_id AND r.vote is not NULL ' +
          'AND r.score > 8.0 ' +
          'ORDER BY imdb_vote DESC LIMIT 10', { type: sequelize.QueryTypes.SELECT})
          .then(function (defaults) {
            if (defaults) {
              defaults = processResult(defaults, userId);
              res.json(defaults);
            }
          })
      }
    });
};

function processResult(results, userId) {
  for (var i in results) {
    var data = [{movie_id: results[i].movie_id, source_id: 1, vote: results[i].imdb_vote, score: results[i].imdb_score},
                {movie_id: results[i].movie_id, source_id: 2, vote: results[i].douban_vote, score: results[i].douban_score},
                {movie_id: results[i].movie_id, source_id: 3, vote: results[i].trakt_vote, score: results[i].trakt_score}];
    results[i].public_ratings= data;
    if (results[i].bookmarks != null) {
      results[i].bookmarks = [{user_id: userId, movie_id: results[i].movie_id}];
    } else {
      results[i].bookmarks = [];
    }
    results[i].user_ratings = [];
    results[i].isShowing = false;
  }
  return results;
}
