var passport = require('passport');
var LocalStrategy = require('passport-local').Strategy;
var User = require('../models/user.js');

// Serialize sessions
passport.serializeUser(function(user, done) {
  done(null, user.id);
});

passport.deserializeUser(function(id, done) {
  User.findOne(id).then(function(user){
    done(null, user);
  }).error(function(err){
    done(err, null);
  });
});

// Use local strategy to create user account
passport.use(new LocalStrategy({
    usernameField: 'username'
  },
  function(username, password, done) {

    User.find({ where: { username : username } }).then(function (user) {
      if (!user) {
        return done(null, false, { message: 'Incorrect email address.' });
      }
      if (!user.validPassword(password)) {
        return done(null, false, { message: 'Incorrect password.' });
      }
      return done(null, user);
    });
  }
));

exports.isAuthenticated = passport.authenticate('local', { session : false });
