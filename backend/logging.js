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
rule.hour = 15;

schedule.scheduleJob(rule, function () {
    // setup email data with unicode symbols
    var mailOptions = {
      from: '"Movie Pigeon" <cs@movie-pigeon.com>', // sender address
      to: 'movie.pigeon@gmail.com', // list of receivers
      subject: '[Movie Pigeon] Logging file', // Subject line
      text: new Date().toLocaleString(), // html body
      attachments: [
        {
          path: '/home/perhaps/.pm2/logs/server-out-0.log'
        },
        {
          path: '/home/perhaps/.pm2/logs/server-error-0.log'
        },
        {
          path: '/home/perhaps/.pm2/logs/cron-out-0.log'
        },
        {
          path: '/home/perhaps/.pm2/logs/cron-error-0.log'
        }
      ]
    };

    // send mail with defined transport object
    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        return console.log(error);
      }
      console.log('Message %s sent: %s', info.messageId, info.response);
    });

    setTimeout(function () {
      pm2.flush(function (err, ret) {
        console.log(err);
        console.log(ret);
      });
    }, 1000);
  }
);

var rule2 = new schedule.RecurrenceRule();
rule2.minute = 59;
rule2.hour = 9;

schedule.scheduleJob(rule2, function () {
    pm2.list(function (err, result) {
      if (err) {
        console.log(err);
        return;
      }

      var data = result;
      var errored = false;
      var text = '';

      for (var i in data) {
        var name = data[i].name;
        var status = data[i].pm2_env.status;
        if (!(status === 'online')) {
          errored = true;
          text = text + name + ":  " + status + "\r\n";
        }
      }

      if (errored) {
        // setup email data with unicode symbols
        text = text + new Date().toLocaleString();
        var mailOptions = {
          from: '"Movie Pigeon" <cs@movie-pigeon.com>', // sender address
          to: 'movie.pigeon@gmail.com', // list of receivers
          subject: '[Movie Pigeon] Server errored', // Subject line
          text: text, // html body
          attachments: [
            {
              path: '/home/perhaps/.pm2/logs/server-error-0.log'
            },
            {
              path: '/home/perhaps/.pm2/logs/cron-error-0.log'
            }
          ]
        };

        // send mail with defined transport object
        transporter.sendMail(mailOptions, (error, info) => {
          if (error) {
            return console.log(error);
          }
          console.log('Message %s sent: %s', info.messageId, info.response);
        });
      }
    });
  }
);
