// Load required packages
var sequelize = require('./db.js');
var DataTypes = require("sequelize");
var User = require('./user.js');
var RatingSource = require('./ratingSource.js');
// Define our cinema schema
var Scale = sequelize.define('scales', {
  weight: {
    type: DataTypes.FLOAT
  }
});

User.belongsTo(RatingSource, {
  through: Scale,
  foreignKey: 'user_id'
});
RatingSource.belongsToMany(User, {
  through: Scale,
  foreignKey: 'source_id'
});

sequelize.sync({});

// Export the model
module.exports = Scale;
