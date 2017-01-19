var User = require('../models/user.js');
var crypto = require('crypto');

exports.retrieveAll = function(onSuccess, onError) {
  User.findAll({}, {raw: true}).then(onSuccess).catch(onError);
};

exports.retrieveById = function(user_id, onSuccess, onError) {
  User.find({where: {id: user_id}}, {raw: true}).then(onSuccess).catch(onError);
};

exports.add = function(user, onSuccess, onError) {
  var username = user.username;
  var password = user.password;

  var shasum = crypto.createHash('sha1');
  shasum.update(password);
  password = shasum.digest('hex');

  User.build({ username: username, password: password })
      .save().then(onSuccess).catch(onError);
}

exports.updateById = function(user, user_id, onSuccess, onError) {
  var id = user_id;
  var username = user.username;
  var password = user.password;

  var shasum = crypto.createHash('sha1');
  shasum.update(password);
  password = shasum.digest('hex');

  User.update({ username: username,password: password},{where: {id: id} })
    .then(onSuccess).catch(onError);
 };

 exports.removeById = function(user_id, onSuccess, onError) {
   User.destroy({where: {id: user_id}}).then(onSuccess).catch(onError);
 };
