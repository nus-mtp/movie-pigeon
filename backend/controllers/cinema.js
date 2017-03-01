// Load required packages
var cinema = require('../models/cinema.js');

// Create endpoint /api/ratings for GET
exports.getCinemas = function (req, res) {
  cinema.getAllCinema().then(function (result) {
    if (result) {
      res.status(200).json(result);
    } else {
      res.status(280).json({status: 'fail', message: 'No Cinemas Found'});
    }
  });
};
