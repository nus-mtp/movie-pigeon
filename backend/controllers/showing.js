var showing = require('../models/showing.js');

exports.getShowingByCinema = function (req, res) {
  showing.getShowingByCinema(req.user.id, req.headers.cinema_id)
    .then(function (result) {
      if (result) {
        res.status(200).json(result);
      } else {
        res.status(280).json({status: 'fail', message: 'No Schedule For Cinema'});
      }
    })
};
