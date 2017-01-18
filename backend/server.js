var express = require('express');
var logger = require('morgan');
var bodyParser = require('body-parser');

var app = express();
app.use(bodyParser.urlencoded({extended: true}));
app.set('port', process.env.PORT || 3355);
app.use(logger('dev'));

var env = app.get('env') == 'development' ? 'dev' : app.get('env');

var User = require('./models/user.js');

// IMPORT ROUTES
// =============================================================================
var router = require('./routes/index.js');

// Middleware to use for all requests
router.use(function(req, res, next) {
	// do logging
	console.log('Something is happening.');
	next();
});

app.use('/api', router);

app.listen(app.get('port'), function() {
  console.log('Express server listening on port ' + app.get('port'));
});
