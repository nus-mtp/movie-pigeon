'use strict';
var nodemailer = require('nodemailer');
var schedule = require('node-schedule');
var pm2 = require('pm2');

// create reusable transporter object using the default SMTP transport
var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'movie.pigeon.customerservice@gmail.com',
    pass: 'hellopigeons'
  }
});

var rule = new schedule.RecurrenceRule();
rule.minute = 59;
rule.hour = 23;

schedule.scheduleJob(rule, function () {
    // setup email data with unicode symbols
    var mailOptions = {
      from: '"Movie Pigeon" <cs@movie-pigeon.com>', // sender address
      to: 'movie.pigeon@gmail.com', // list of receivers
      subject: '[Movie Pigeon] Logging file', // Subject line
      text: new Date().toLocaleString(), // html body
      attachments: [{
        path: '/README.md'
      }]
    };

    // send mail with defined transport object
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        return console.log(error);
      }
      console.log('Message %s sent: %s', info.messageId, info.response);
    });

    pm2.flush('server', function (err) {
      console.log(err);
    });

    pm2.flush('cron', function (err) {
      console.log(err);
    });
  }
);
