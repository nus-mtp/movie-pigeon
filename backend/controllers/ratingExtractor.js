var request = require('request');
var rate = require('../proxy/rate.js');
var User = require('../proxy/user.js');

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
  User.getUserByEmail(userEmail)
    .then(function (user) {
      (function next(index) {
        if (index === data.length) {
          return;
        }
        var rating = data[index].rating;
        var movieId = data[index].movie.ids.imdb;

        rate.getSpecificRate(user.id, movieId)
          .then(function (ratings) {
            if (ratings) {
              console.log('fail');
            } else {
              rate.postRates(rating, movieId, user.id)
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
  var username = req.body.username;
  var password = req.body.password;
  var email = req.body.email;

  var result = false;

  User.getUserByEmail(email)
    .then(function (users) {
      if (users) {
        res.status(409).json({
          status: 'fail',
          message: 'User Existed'
        });
      } else {
        User.saveUser(email, username, password)
          .then(function () {
            result = true;
            res.status(200).json({
              status: 'success',
              message: 'User Created'
            });

          })
          .catch(function (err) {
            res.send(err);
          });
      }
    });

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
  }, 500);
};

exports.checkTraktUser = function (req, res) {
  var id = req.headers.username;
  checkUsername(id, function (err, body) {
    if (err) {
      console.log(err);
    } else {
      if (body === null) {
        res.status(404).send(false);
      } else {
        res.status(200).send(true);
      }
    }
  });
};
