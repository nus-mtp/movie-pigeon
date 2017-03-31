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
  provider: {
    type: DataTypes.STRING
  },
  location_x: {
    type: DataTypes.FLOAT
  },
  location_y: {
    type: DataTypes.FLOAT
  },
  displayed_name: {
    type: DataTypes.STRING
  }
});

sequelize.sync({});
// Export the model
module.exports = Cinema;
