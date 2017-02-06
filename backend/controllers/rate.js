// Load required packages
var Rate = require('../models/history.js');

// Create endpoint /api/ratings for POST
exports.postRates = function (req, res) {
  var movieId = req.body.movieId;
  var score = req.body.score;
  var userId = req.user.id;
  // Save the rating and check for errors
  Rate.build({score: score, movie_id: movieId, user_id: userId})
      .save().then(function (success) {
        res.json({message: 'Ratings successfully posted!'});
      });
};

// Create endpoint /api/ratings for GET
exports.getRates = function (req, res) {
  // Use the Ratings model to find all clients
  Rate.findAll({where: {user_id: req.user.id}}).then(function(ratings){
    res.json(ratings);
  });
};
