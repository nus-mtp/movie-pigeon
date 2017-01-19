var sequelize = require('./db.js');
var crypto = require('crypto');
var DataTypes = require("sequelize");

var User = sequelize.define('users', {
    username: DataTypes.STRING,
    password: DataTypes.STRING
},
{
  instanceMethods: {
    validPassword: function(password) {
      var shasum = crypto.createHash('sha1');
      shasum.update(password);
      password = shasum.digest('hex');
      return password == this.password;
    }
  }
}
);

module.exports = User;
