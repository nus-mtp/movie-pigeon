var recommendation = require('../proxy/recommendation');

// Create endpoint /api/recommendations for GET
module.exports.getRecommendation = function (req, res) {
  var userId = req.user.id;

  recommendation.getAllRecommendation(userId)
    .then(function (result) {
      if (result) {
        res.json(result)
      } else {
        res.json({
          status: 'fail',
          message: 'No Recommendations'
        });
      }
    });
};

