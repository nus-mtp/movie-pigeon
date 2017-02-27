var User = require('../models/user.js');
var crypto = require('crypto');

exports.postUser = function (req, res) {
  var username = req.body.username;
  var password = req.body.password;
  var email = req.body.email;

  var shasum = crypto.createHash('sha1');
  shasum.update(password);
  password = shasum.digest('hex');

  User.find({where: {email: email}})
    .then(function (users) {
      if (users) {
        res.json({status: 'fail', message: 'User Existed'});
        return false;
      } else {
        User.build({email: email, username: username, password: password})
          .save()
          .then(function () {
            res.json({status: 'success', message: 'User Created'});
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
      res.json({status: 'fail', message: 'Same Username'});
    } else {
      user.updateAttributes({
        username: username
      }).then(function () {
        res.json({status: 'success', message: 'Username Updated'});
      });
    }
  } else {
    res.json({status: 'fail', message: 'No Username Provided'});
  }
};

exports.updatePassword = function (req, res) {
  var password = req.body.password;
  var user = req.user;

  if (password) {
    var shasum = crypto.createHash('sha1');
    shasum.update(password);
    password = shasum.digest('hex');

    if (user.password === password) {
      res.json({status: 'fail', message: 'Same Password'});
    } else {
      user.updateAttributes({
        password: password
      }).then(function () {
        res.json({status: 'success', message: 'Password Updated'});
      });
    }
  } else {
    res.json({status: 'fail', message: 'No Password Provided'});
  }
};

exports.removeById = function (user_id, onSuccess, onError) {
  User.destroy({where: {id: user_id}}).then(onSuccess).catch(onError);
};
