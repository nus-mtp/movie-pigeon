// Load required packages
var bookmarks = require('../proxy/bookmark.js');
var utils = require('./utils');
// Create endpoint /api/ratings for POST
exports.postBookmarks = function (req, res) {
  var movieId = req.body.movieId;
  var userId = req.user.id;

  bookmarks.getSpecificBookmark(userId, movieId)
    .then(function (bookmarkResults) {
      if (bookmarkResults) {
        res.json({
          status: 'fail',
          message: 'Bookmark Existed'
        });
      } else {
        // Save the bookmark and check for errors
        bookmarks.postBookmark(movieId, userId)
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

  bookmarks.getSpecificBookmark(userId, movieId)
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
    .catch(function (err) {
      console.log(err);
    });
};

// Create endpoint /api/bookmarks for GET
exports.getBookmarks = function (req, res) {

  bookmarks.getAllBookmarks(req.user.id)
    .then(function (movies) {
      utils.hasSchedule(movies);
      res.json(movies);
    });
};
