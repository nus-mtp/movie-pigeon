var User = require('../models/user.js');

module.exports.getUserByEmail = function (email) {
  return User.find({
    where: {
      email: email
    }
  });
};

module.exports.saveUser = function (email, username, password) {
  return User.create({
    email: email,
    username: username,
    password: User.getHashedPassword(password)
  })
};

module.exports.updateUserUsername = function (user, username) {
  return user.updateAttributes({
    username: username
  })
};

module.exports.updateUserPassword = function (user, password) {
  return user.updateAttributes({
    password: User.getHashedPassword(password)
  })
};
