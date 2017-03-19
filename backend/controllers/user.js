var User = require('../proxy/user.js');
var UserModel = require('../models/user.js');

//Create endpoint for POST /api/users
exports.postUser = function (req, res) {
  var username = req.body.username;
  var password = req.body.password;
  var email = req.body.email;

  //Check if duplicate email
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
            flag = true;
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
};

//Create endpoint for GET /api/users
exports.getUser = function (req, res) {
  res.json({email: req.user.email, username: req.user.username});
};

//Create endpoint ofr PUT /api/users/username
exports.updateUsername = function (req, res) {
  var username = req.body.username;
  var user = req.user;

  if (username) {
    if (user.username === username) {
      res.json({
        status: 'fail',
        message: 'Same Username'
      });
    } else {
      User.updateUserUsername(user, username)
        .then(function () {
          res.json({
            status: 'success',
            message: 'Username Updated'
          });
        });
    }
  } else {
    res.json({
      status: 'fail',
      message: 'No Username Provided'
    });
  }
};

//Create endpoint for PUT /api/users/password
exports.updatePassword = function (req, res) {
  var password = req.body.password;
  var user = req.user;

  if (password) {
    if (user.password === UserModel.getHashedPassword(password)) {
      res.json({
        status: 'fail',
        message: 'Same Password'
      });
    } else {
      User.updateUserPassword(user, password)
        .then(function () {
          res.json({
            status: 'success',
            message: 'Password Updated'
          });
        });
    }
  } else {
    res.json({
      status: 'fail',
      message: 'No Password Provided'
    });
  }
};
