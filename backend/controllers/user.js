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
        return res.json({status: 'fail', message: 'User Existed'});
      } else {
        User.build({email: email, username: username, password: password})
          .save()
          .then(function () {
            res.json({status: 'success', message: 'User Created'});
          })
          .catch(function (err) {
            res.send(err);
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

exports.updateById = function (user, userId, onSuccess, onError) {
  var id = userId;
  var username = user.username;
  var password = user.password;

  var shasum = crypto.createHash('sha1');
  shasum.update(password);
  password = shasum.digest('hex');

  User.update({username: username, password: password}, {where: {id: id}})
    .then(onSuccess).catch(onError);
};

exports.removeById = function (user_id, onSuccess, onError) {
  User.destroy({where: {id: user_id}}).then(onSuccess).catch(onError);
};
