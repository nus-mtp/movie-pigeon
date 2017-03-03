// Load required packages
var bookmarks = require('../models/bookmarks.js');
var movie = require('../models/movie.js');
var publicRate = require('../models/PublicRate.js');
var RatingSource = require('../models/ratingSource.js');
var UserRating = require('../models/history.js');

// Create endpoint /api/ratings for POST
exports.postBookmarks = function (req, res) {
  var movieId = req.body.movieId;
  var userId = req.user.id;

  bookmarks.find({
    where: {
      user_id: userId,
      movie_id: movieId
    }
  }).then(function (bookmarkResults) {
    if (bookmarkResults) {
      res.json({
        status: 'fail',
        message: 'Bookmark Existed'
      });
    } else {
      // Save the bookmark and check for errors
      bookmarks.build({
        movie_id: movieId,
        user_id: userId
      })
        .save()
        .then(function () {
          res.json({
            status: 'success',
            message: 'Bookmark Posted'
          });
        });
    }
  });
};

exports.deleteBookmarks = function (req, res) {
  var movieId = req.body.movieId;
  var userId = req.user.id;

  bookmarks.find({
    where: {
      movie_id: movieId,
      user_id: userId
    }
  })
    .then(function (bookmarkResult) {
      if (bookmarkResult) {
        bookmarkResult.destroy()
          .then(function () {
            res.json({
              status: 'success',
              message: 'Bookmark Deleted'
            });
          })
          .catch(function (err) {
            console.log(err);
          });
      } else {
        res.json({
          status: 'fail',
          message: 'Bookmark Not Found'
        });
      }
    })
    .catch(function () {
      console.log(err);
    });
};

// Create endpoint /api/bookmarks for GET
exports.getBookmarks = function (req, res) {
  // bookmarks.findAll({
  //   where: {
  //     user_id: req.user.id
  //   },
  //   include: [{
  //     model: movie
  //   }]
  // })
  //   .then(function (results) {
  //     res.json(results);
  //   });

  movie.findAll({
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
          user_id: req.user.id
        },
        required: true
      },
      {
        model: UserRating,
        where: {
          user_id: req.user.id
        },
        required: false
      }
    ]
  }).then(function (movies) {
    res.json(movies);
  });
};
