// Load required packages
var Client = require('../models/client.js');

// Create endpoint /api/client for POST
exports.postClients = function (req, res) {
  var name = req.body.name;
  var id = req.body.id;
  var secret = req.body.secret;
  var userId = req.user.email;
  // Save the client and check for errors
  Client.create({name: name, id: id, secret: secret, userId: userId})
    .then(function () {
      res.json({
        status: 'Success',
        message: 'Client Created'
      });
    });
};
