// Load required packages
var Movie = require('../proxy/movie.js');

function processSearchString(searchString) {
  searchString = searchString.trim().replace(' ', '%');
  searchString = '%' + searchString + '%';
  return searchString;
}

// Create endpoint /api/movie for GET
exports.getMoviesByTitle = function (req, res) {
  // Use the Client model to find all clients
  var searchString = processSearchString(req.headers.title);
  Movie.getMovieByTitleCount(searchString)
    .then(function (count) {
      Movie.getMovieByTitle(req.user.id, searchString, req.headers.offset, req.headers.limit)
        .then(function (movies) {
          res.json({count: count, raw: movies});
        }).catch(function (err) {
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
