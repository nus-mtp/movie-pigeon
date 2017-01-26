var sequelize = require('./db.js');
var crypto = require('crypto');
var DataTypes = require("sequelize");

var client = sequelize.define('clients', {
    name: {
      type: DataTypes.STRING
    },
    id: {
      type: DataTypes.STRING
    },
    secret: {
      type: DataTypes.STRING
    },
    userId: {
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

module.exports = client;
