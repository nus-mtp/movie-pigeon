// Load required packages
var rate = require('../proxy/rate.js');
var movie = require('../proxy/movie.js');

// Create endpoint /api/ratings for POST
exports.postRates = function (req, res) {
  var movieId = req.body.movieId;
  var score = parseFloat(req.body.score) || -1;
  var userId = req.user.id;

  if (score < 0 || score > 10) {
    res.json({status: 'fail', message: 'Invalid Score'});
    return;
  }

  movie.getMovieById(movieId)
    .then(function (movie) {
      if (movie) {
        rate.getSpecificRate(userId, movieId)
          .then(function (ratings) {
            if (ratings) {
              rate.updateRates(ratings, score)
                .then(function () {
                  return res.json({
                    status: 'success',
                    message: 'Ratings Updated'
                  });
                });
            } else {
              // Save the rating and check for errors
              rate.postRates(score, movieId, userId)
                .then(function () {
                  res.json({
                    status: 'success',
                    message: 'Ratings Posted!'
                  });
                });
            }
          });
      } else {
        res.json({
          status: 'fail',
          message: 'Invalid MovieId'
        });
      }
    });
};

// Create endpoint /api/ratings for GET
exports.getRates = function (req, res) {
  rate.getAllRates()
    .then(function (movies) {
      res.json(movies);
    });
};
