// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
// Define our token schema
var RatingSource = sequelize.define('ratingsources', {
  source_id: {
    type: DataTypes.STRING,
    allowNull: false,
    primaryKey: true
  },
  source_name: {
    type: DataTypes.STRING
  }
});

// Export the Mongoose model
module.exports = RatingSource;
