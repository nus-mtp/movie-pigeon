var Cinema = require('../models/cinema');

module.exports.getAllCinema = function () {
  return Cinema.findAll();
};
