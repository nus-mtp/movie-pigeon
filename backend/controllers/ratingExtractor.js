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
        res.json({
          status: 'fail',
          message: 'User Existed'
        });
      } else {
        User.saveUser(email, username, password)
          .then(function () {
            result = true;
            res.json({
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
        res.send(false);
      } else {
        res.send(true);
      }
    }
  });
};

function getTmdbToken(callback) {
  var url = 'https://api.themoviedb.org/3/authentication/token/new?api_key=c3753c1a33a753893fefdd2e7f3b0dfa';
  request({
    method: 'GET',
    url: url,
    headers: {
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

function checkTmdbUser(username, password, request_token, callback) {
  var url = 'https://api.themoviedb.org/3/authentication/token/validate_with_login' +
    '?api_key=c3753c1a33a753893fefdd2e7f3b0dfa&username='+ username +'&password='+ password + '&request_token=' + request_token;
  request({
    method: 'GET',
    url: url,
    headers: {
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

function getTmdbSessionId(request_token, callback) {
  var url = 'https://api.themoviedb.org/3/authentication/session/new?api_key=c3753c1a33a753893fefdd2e7f3b0dfa&request_token=' + request_token;
  request({
    method: 'GET',
    url: url,
    headers: {
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

function  getTmdbRatings(sessionId, callback) {
  var url = 'https://api.themoviedb.org/3/account/{account_id}/rated/movies' +
    '?api_key=c3753c1a33a753893fefdd2e7f3b0dfa&language=en-US&session_id='+ sessionId +'&sort_by=created_at.asc';
  request({
    method: 'GET',
    url: url,
    headers: {
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

exports.checkTmdbUser = function (req, res) {
  var username = req.headers.username;
  var password = req.headers.password;
  getTmdbToken(function (err, body) {
    console.log(body);
    if (err) {
      res.json({status: 'fail', message: 'TMDb server unavailable'});
    } else {
      checkTmdbUser(username, password, body.request_token, function (err, result) {
        if (err) {
          res.json(false);
        } else {
          if (result.success === true) {
            res.json(true);
          }
        }
      });
    }
  });
};

exports.getTmdbRatings = function (req, res) {
  var username = req.headers.username;
  var password = req.headers.password;
  getTmdbToken(function (err, body) {
    console.log(body);
    if (err) {
      res.json({status: 'fail', message: 'TMDb server unavailable'});
    } else {
      checkTmdbUser(username, password, body.request_token, function (err, result) {
        if (err) {
          res.status(401).json(false);
        } else {
          if (result.success === true) {
            getTmdbSessionId(result.request_token, function (err, content) {
              if (err) {
                console.log(err);
              } else {
                getTmdbRatings(content.session_id, function (err, ratings) {
                  if (err) {
                    console.log(err);
                  } else {
                    console.log(ratings);
                  }
                });
              }
            })
          }
        }
      });
    }
  });
};
