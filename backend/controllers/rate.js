// Load required packages
var rate = require('../models/history.js');
var movie = require('../models/movie.js');
var PublicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');

// Create endpoint /api/ratings for POST
exports.postRates = function (req, res) {
  var movieId = req.body.movieId;
  var score = parseFloat(req.body.score) || -1;
  var userId = req.user.id;

  if (score < 0 || score > 10) {
    res.json({status: 'fail', message: 'Invalid Score'});
    return;
  }

  movie.find({
    where: {
      movie_id: movieId
    }
  }).then(
    function (movie) {
      if (movie) {
        rate.find({
          where: {
            movie_id: movieId,
            user_id: userId
          }
        }).then(function (ratings) {
          if (ratings) {
            ratings.updateAttributes({
              score: score
            }).then(function () {
              return res.json({
                status: 'success',
                message: 'Ratings Updated'
              });
            });
          } else {
            // Save the rating and check for errors
            rate.build({
              score: score,
              movie_id: movieId,
              user_id: userId
            })
              .save().then(function (success) {
              res.json({
                status: 'success',
                message: 'Ratings Posted!'
              });
            });
          }
        });
      } else {
        res.json({status: 'fail', message: 'Invalid MovieId'});
      }
    });
};

// Create endpoint /api/ratings for GET
exports.getRates = function (req, res) {
  // Use the Ratings model to find all clients
  // rate.findAll({
  //   where: {
  //     user_id: req.user.id
  //   },
  //   include: [{
  //     model: movie
  //   }]
  // })
  //   .then(function (ratings) {
  //     res.json(ratings);
  //   });

  movie.findAll({
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
          user_id: req.user.id
        },
        required: true
      }
    ]
  }).then(function (movies) {
    res.json(movies);
  });
};
