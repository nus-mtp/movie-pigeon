var sequelize = require('./db.js');
var crypto = require('crypto');
var DataTypes = require("sequelize");

var client = sequelize.define('clients', {
    name: DataTypes.STRING,
    id: DataTypes.STRING,
    secret: DataTypes.STRING,
    userId: DataTypes.STRING
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

module.exports = client;
