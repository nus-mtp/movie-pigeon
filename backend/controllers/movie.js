// Load required packages
var Movie = require('../proxy/movie.js');

// Create endpoint /api/movie for GET
exports.getMoviesByTitle = function (req, res) {
  // Use the Client model to find all clients
  Movie.getMovieByTitleCount(req.headers.title)
    .then(function (count) {
      Movie.getMovieByTitle(req.user.id, req.headers.title, req.headers.offset, req.headers.limit)
        .then(function (movies) {
          res.json({count: count, raw: movies});
        }).catch(function (err) {
          console.log(err);
        }
      );
    });
};

// Create endpoint /api/movie for GET
exports.getMoviesById = function (req, res) {
  // Use the Client model to find all clients
  Movie.find({where: {id: req.headers.id}}).then(function (movies) {
    res.json(movies);
  }).catch(function (err) {
    res.send(err);
  });
};

// Create endpoint /api/movie for GET
exports.getMoviesByProductionYear = function (req, res) {
  // Use the Client model to find all clients
  Movie.find({where: {productionYear: req.headers.productionYear}})
    .then(function (movies) {
      res.json(movies);
    }).catch(function (err) {
    res.send(err);
  });
};
