var Bookmark = require('./bookmarks.js');
var Cinema = require('./cinema.js');
var Client = require('./client.js');
var Code = require('./code.js');
var sequelize = require('./db.js');
var history = require('./history.js');
var movie = require('./movie.js');
var PublicRate = require('./PublicRate.js');
var ratingSource = require('./ratingSource.js');
var recommendation = require('./recommendation.js');
var scale = require('./scale.js');
var showing = require('./showing.js');
var token = require('./token.js');
var user = require('./user.js');

sequelize.sync({});
