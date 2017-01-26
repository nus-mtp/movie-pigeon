var sequelize = require('./db.js');
var crypto = require('crypto');
var DataTypes = require("sequelize");

var User = sequelize.define('users', {
    username: {
      type: DataTypes.STRING,
      unique: true,
      primaryKey: true
    },
    password: {
      type: DataTypes.STRING
    }
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

sequelize.sync({});

module.exports = User;
