// Load required packages
var sequelize = require('./db.js');
var User = require('./user.js');
var Movie = require('./movie.js');
var DataTypes = require('sequelize');
// Define our bookmark schema
var Bookmark = sequelize.define('bookmarks', {
  user_id: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  movie_id: {
    type: DataTypes.STRING,
    primaryKey: true
  }
});

User.hasMany(Bookmark, {foreignKey: 'user_id'});
Bookmark.belongsTo(User, {
  foreignKey: 'user_id',
  targetKey: 'id'
});

Movie.hasMany(Bookmark, {foreignKey: 'movie_id'});
Bookmark.belongsTo(Movie, {foreignKey: 'movie_id', targetKey: 'movie_id'});

sequelize.sync({});

// Export the model
module.exports = Bookmark;
