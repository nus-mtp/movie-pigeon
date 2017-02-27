var request = require('request');
var rate = require('../models/history.js');
var user = require('../controllers/user.js');
var User = require('../models/user.js');

function getRatings(id, callback) {
  var url = 'https://api.trakt.tv/users/' + id + '/ratings/movies';
  request({
    method: 'GET',
    url: url,
    headers: {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }
  }, function (error, response, body) {
    if (error || response.statusCode !== 200) {
      return callback(error || {statusCode: response.statusCode});
    }
    callback(null, JSON.parse(body));
  });
}

function checkUsername(id, callback) {
  var url = 'https://api.trakt.tv/users/' + id;
  request({
    method: 'GET',
    url: url,
    headers: {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '411a8f0219456de5e3e10596486c545359a919b6ebb10950fa86896c1a8ac99b'
    }
  }, function (error, response, body) {
    if (response.statusCode === 404) {
      return callback(null, null);
    }
    if (error || response.statusCode !== 200) {
      return callback(error || {statusCode: response.statusCode});
    }
    callback(null, JSON.parse(body));
  });
}

function processData(userEmail, body) {
  var data = body;
  User.find({
    where: {
      email: userEmail
    }
  }).then(function (user) {
    (function next(index) {
      if (index === data.length) {
        return;
      }
      var rating = data[index].rating;
      var movieId = data[index].movie.ids.imdb;

      rate.find({
        where: {
          user_id: user.id,
          movie_id: movieId
        }
      })
        .then(function (ratings) {
          if (ratings) {
            console.log('fail');
          } else {
            rate.create({
              user_id: user.id,
              movie_id: movieId,
              score: rating
            })
              .then(function () {
                next(index + 1);
                return;
              })
              .catch(function (err) {
                console.log(err);
              });
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    })(0);
  });

}

exports.getTraktRatings = function (req, res) {
  var id = req.body.traktTVId;
  var result = user.postUser(req, res);
  setTimeout(function () {
    if (result === true) {
      getRatings(id, function (err, body) {
        if (err) {
          console.log(err);
        } else {
          processData(req.body.email, body);
        }
      });
    }
  }, 800);
};

exports.checkTraktUser = function (req, res) {
  var id = req.headers.username;
  checkUsername(id, function (err, body) {
    if (err) {
      console.log(err);
    } else {
      if (body === null) {
        res.send(false);
      } else {
        res.send(true);
      }
    }
  });
};
