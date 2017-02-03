var Sequelize = require('sequelize');

// db config
var env = process.env.NODE_ENV ? process.env.NODE_ENV : "dev";
var config = require('../database.json')[env];
var password = config.password ? config.password : null;

module.exports = new Sequelize(
	config.database,
	config.user,
	config.password,
	{
    dialect: config.driver,
    logging: console.log,
		define: {
			timestamps: false
		}
	}
);
