var recommendation = require('../models/recommendation');

module.exports.getAllRecommendation = function (userId) {
  return recommendation.findAll({
    where: {
      user_id: userId
    }
  })
};
