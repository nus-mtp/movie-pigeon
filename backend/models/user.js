var sequelize = require('./db.js');

var crypto = require('crypto');
var DataTypes = require("sequelize");

var User = sequelize.define('users', {
    username: DataTypes.STRING,
    password: DataTypes.STRING
  }, {
    instanceMethods: {
      retrieveAll: function(onSuccess, onError) {
			User.findAll({}, {raw: true}).then(onSuccess).catch(onError);
	  },
      retrieveById: function(user_id, onSuccess, onError) {
			User.find({where: {id: user_id}}, {raw: true}).then(onSuccess).catch(onError);
	  },
      add: function(onSuccess, onError) {
			var username = this.username;
			var password = this.password;

			var shasum = crypto.createHash('sha1');
			shasum.update(password);
			password = shasum.digest('hex');

			User.build({ username: username, password: password })
			    .save().then(onSuccess).catch(onError);
	   },
	  updateById: function(user_id, onSuccess, onError) {
			var id = user_id;
			var username = this.username;
			var password = this.password;

			var shasum = crypto.createHash('sha1');
			shasum.update(password);
			password = shasum.digest('hex');

			User.update({ username: username,password: password},{where: {id: id} })
				.then(onSuccess).catch(onError);
	   },
      removeById: function(user_id, onSuccess, onError) {
				User.destroy({where: {id: user_id}}).then(onSuccess).catch(onError);
	  	}
    }
  });

module.exports = User;
