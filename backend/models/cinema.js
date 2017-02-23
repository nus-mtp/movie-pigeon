// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
// Define our cinema schema
var Cinema = sequelize.define('cinemas', {
  cinema_id: {
    type: DataTypes.INTEGER,
    autoIncrement: true,
    primaryKey: true
  },
  cinema_name: {
    type: DataTypes.STRING,
    allowNull: true,
    unique: true
  },
  url: {
    type: DataTypes.TEXT
  }
});

sequelize.sync({});
// Export the model
module.exports = Cinema;
