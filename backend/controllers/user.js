var User = require('../proxy/user.js');
var UserModel = require('../models/user.js');

exports.postUser = function (req, res) {
  var username = req.body.username;
  var password = req.body.password;
  var email = req.body.email;

  User.getUserByEmail(email)
    .then(function (users) {
      if (users) {
        res.json({
          status: 'fail',
          message: 'User Existed'
        });
        return false;
      } else {
        User.saveUser(email, username, password)
          .then(function () {
            res.json({
              status: 'success',
              message: 'User Created'
            });
            return true;
          })
          .catch(function (err) {
            res.send(err);
            return false;
          });
      }
    });
};

var retrieveAll = function (onSuccess, onError) {
  User.findAll({}, {raw: true}).then(onSuccess).catch(onError);
};

exports.getUser = function (req, res) {
  retrieveAll(function (users) {
    if (users) {
      res.json(users);
    } else {
      res.send(401, 'User not found');
    }
  }, function (err) {
    res.send('User not found');
  });
};

exports.retrieveById = function (userId, onSuccess, onError) {
  User.find({where: {id: userId}}, {raw: true}).then(onSuccess).catch(onError);
};

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

exports.removeById = function (user_id, onSuccess, onError) {
  User.destroy({where: {id: user_id}}).then(onSuccess).catch(onError);
};
