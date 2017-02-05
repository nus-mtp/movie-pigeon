// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');

// Define our token schema
var accessCode = sequelize.define('codes', {
  value: {
    type: DataTypes.STRING
  },
  redirectUri: {
    type: DataTypes.STRING
  },
  userId: {
    type: DataTypes.STRING
  },
  clientId: {
    type: DataTypes.STRING
  }
});


sequelize.sync({});

// Export the Mongoose model
module.exports = accessCode;
