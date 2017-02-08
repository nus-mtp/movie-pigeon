// Load required packages
var sequelize = require('./db.js');
var DataTypes = require('sequelize');
var User = require('./user.js');
var RatingSource = require('./ratingSource.js');
// Define our scale schema
var Scale = sequelize.define('scales', {
  user_id: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  source_id: {
    type: DataTypes.STRING,
    primaryKey: true
  },
  weight: {
    type: DataTypes.FLOAT
  }
});

RatingSource.hasMany(Scale, {foreignKey: 'source_id'});
Scale.belongsTo(RatingSource, {foreignKey: 'source_id', targetKey: 'source_id'});

User.hasMany(Scale, {foreignKey: 'user_id'});
Scale.belongsTo(User, {foreignKey: 'user_id', targetKey: 'id'});

sequelize.sync({});
// Export the model
module.exports = Scale;
