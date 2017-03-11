var express = require('express');
var router = express.Router();
var userControl = require('../controllers/user.js');
var authController = require('../controllers/auth');
var oauth2Controller = require('../controllers/oauth2');
var clientController = require('../controllers/client');
var bookmarkController = require('../controllers/bookmark');
var movieController = require('../controllers/movie');
var ratingController = require('../controllers/rate');
var thirdPartyController = require('../controllers/ratingExtractor.js');
var emailService = require('../email/email');
var cinemaController = require('../controllers/cinema.js');
var showingController = require('../controllers/showing.js');
var recommendationController = require('../controllers/recommendation');
// on routes that end in /users
// ----------------------------------------------------
router.route('/users')
  .post(userControl.postUser)
  .get(authController.isAuthenticated, userControl.getUser);

router.route('/users/username')
  .put(authController.isAuthenticated, userControl.updateUsername);

router.route('/users/password')
  .put(authController.isAuthenticated, userControl.updatePassword);

router.route('/users/resetPassword')
  .post(emailService.buildResetRequest);

router.post('/users/login', authController.isAuthenticated, function (req, res) {
  return res.send('login successful');
});

// Create endpoint handlers for /clients
router.route('/clients')
  .post(authController.isAuthenticated, clientController.postClients)
  .get(authController.isAuthenticated, clientController.getClients);

// Create endpoint handlers for oauth2 authorize
router.route('/oauth2/authorize')
  .get(authController.isAuthenticated, oauth2Controller.authorization)
  .post(authController.isAuthenticated, oauth2Controller.decision);

router.route('/oauth2/authorize/transactionId')
  .post(authController.isAuthenticated, oauth2Controller.authorization);

// Create endpoint handlers for oauth2 token
router.route('/oauth2/token')
  .post(authController.isClientAuthenticated, oauth2Controller.token);

router.route('/movies/id')
  .get(authController.isAuthenticated, movieController.getMoviesById);
router.route('/movies/title')
  .get(authController.isAuthenticated, movieController.getMoviesByTitle);
router.route('/movies/year')
  .get(authController.isAuthenticated,
    movieController.getMoviesByProductionYear);

router.route('/bookmarks')
  .post(authController.isAuthenticated, bookmarkController.postBookmarks)
  .get(authController.isAuthenticated, bookmarkController.getBookmarks)
  .delete(authController.isAuthenticated, bookmarkController.deleteBookmarks);

router.route('/ratings')
  .post(authController.isAuthenticated, ratingController.postRates)
  .get(authController.isAuthenticated, ratingController.getRates);

router.route('/recommendations')
  .get(authController.isAuthenticated, recommendationController.getRecommendation);

router.route('/traktTV')
  .get(thirdPartyController.checkTraktUser)
  .post(thirdPartyController.getTraktRatings);

router.route('/cinemas')
  .get(authController.isAuthenticated, cinemaController.getCinemas);

router.route('/showing')
  .get(authController.isAuthenticated, showingController.getShowingByCinema);

module.exports = router;
