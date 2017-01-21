// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
// Define our token schema
var Token = sequelize.define('token', {
  value: DataTypes.STRING,
  userId: DataTypes.STRING,
  clientId: DataTypes.STRING
});

// Export the Mongoose model
module.exports = Token;
