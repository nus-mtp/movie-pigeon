var express = require('express');
var router = express.Router();
var userControl = require('../controllers/user.js');
var User = require('../models/user.js');
var authController = require('../controllers/auth');

var passport = require('passport');
// on routes that end in /users
// ----------------------------------------------------
router.route('/users')

// create a user (accessed at POST http://localhost:8080/api/users)
.post(function(req, res) {
	var username = req.body.username; //bodyParser does the magic
	var password = req.body.password;

	var user = User.build({ username: username, password: password });

	userControl.add(user, function(success){
		res.json({ message: 'User created!' });
	},
	function(err) {
		res.send(err);
	});
})

// get all the users (accessed at GET http://localhost:8080/api/users)
.get(authController.isAuthenticated, function(req, res) {
	var user = User.build();

	userControl.retrieveAll(function(users) {
		if (users) {
		  res.json(users);
		} else {
		  res.send(401, "User not found");
		}
		}, function(error) {
			res.send("User not found");
	  });
});


// on routes that end in /users/:user_id
// ----------------------------------------------------
router.route('/users/:user_id')

// update a user (accessed at PUT http://localhost:8080/api/users/:user_id)
.put(authController.isAuthenticated, function(req, res) {
	var user = User.build();

	user.username = req.body.username;
	user.password = req.body.password;

	userControl.updateById(user, req.params.user_id, function(success) {
		console.log(success);
		if (success) {
			res.json({ message: 'User updated!' });
		} else {
		  res.send(401, "User not found");
		}
	  }, function(error) {
		res.send("User not found");
	  });
})

// get a user by id(accessed at GET http://localhost:8080/api/users/:user_id)
.get(authController.isAuthenticated, function(req, res) {
	var user = User.build();

	userControl.retrieveById(req.params.user_id, function(users) {
		if (users) {
		  res.json(users);
		} else {
		  res.send(401, "User not found");
		}
	  }, function(error) {
		res.send("User not found");
	  });
})

// delete a user by id (accessed at DELETE http://localhost:port/api/users/:user_id)
.delete(authController.isAuthenticated, function(req, res) {
	var user = User.build();

	user.removeById(req.params.user_id, function(users) {
		if (users) {
		  res.json({ message: 'User removed!' });
		} else {
		  res.send(401, "User not found");
		}
	  }, function(error) {
		res.send("User not found");
	  });
});

/*
router.post('/users/login', passport.authenticate('local'),
	function(req, res) {
  	res.send(req.body.username + 'login successful!');
	},
	function(err, req, res, next) {
		// handle error
		if (req.xhr) { return res.json(err); }
	}
);
*/
router.post('/users/login', function(req, res, next) {
  passport.authenticate('local', function(err, user, info) {
    if (err) { return next(err); }
    if (!user) { return res.send('login fail'); }
    req.logIn(user, function(err) {
      if (err) { return next(err); }
      return res.send(user.username + 'login successful');
    });
  })(req, res, next);
});

module.exports = router;
