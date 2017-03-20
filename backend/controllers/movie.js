// Load required packages
var Movie = require('../proxy/movie.js');
var _ = require('underscore');
var dateFormat = require('dateformat');
var utils = require('./utils');
var moment = require('moment');
var timSort = require('timsort');

// Create endpoint /api/movies/title for GET
exports.getMoviesByTitle = function (req, res) {
  // Use the Client model to find all clients
  Movie.getMovieByTitleCount(req.headers.title)
    .then(function (count) {
      Movie.getMovieByTitle(req.user.id, req.headers.title, req.headers.offset, req.headers.limit)
        .then(function (movies) {
          movies = utils.hasSchedule(movies);
          res.json({count: count, raw: movies});
        }).catch(function (err) {
          console.log(err);
        }
      );
    });
};

// Create endpoint /api/movies/showing for GET
exports.getShowingMovieByTitle = function (req, res) {
  Movie.getShowingMovieByTitle(req.user.id, req.headers.title)
    .then(function (movies) {
      res.json(movies);
    }).catch(function (err) {
      console.log(err);
    }
  );
};

/**
 * Parse the schedule in the movies.
 *
 * - split showing timestamp into date and time
 * - remove redundant info in the result. (i.e. cinema, movie_id and raw schedule)
 *
 */
function parseSchedule(schedules) {
  for (var i in schedules) {
    schedules[i].schedule.setHours(schedules[i].schedule.getHours() - 8);
    schedules[i].dataValues.schedule = schedules[i].schedule;
    schedules[i].dataValues.date = dateFormat(schedules[i].schedule, 'yyyy-mm-dd');
    schedules[i].dataValues.time = dateFormat(schedules[i].schedule, 'HH:MM:ss');
    schedules[i].dataValues.cinema_name = schedules[i].cinema.cinema_name;
    schedules[i].date = schedules[i].dataValues.date;
    schedules[i].time = schedules[i].dataValues.time;
    schedules[i].cinema_name = schedules[i].cinema.cinema_name;
    delete schedules[i].dataValues.cinema;
    delete schedules[i].dataValues.movie_id;
    delete schedules[i].dataValues.schedule;
  }
  return schedules;
}

/**
 * Sort the parsed schedule.
 *
 * - Movie schedule are sorted in the order: Date --> Cinema --> Type --> Time
 */
function typeCmp(a, b) {
  return String(a.type).localeCompare(b.type);
}function cinemaCmp(a, b) {
  return String(a.cinema_name).localeCompare(b.cinema_name);
}function dateCmp(a, b) {
  return String(a.date).localeCompare(b.date);
}function timeCmp(a, b) {
  return String(a.time).localeCompare(b.time);
}
function sortSchedule(schedules) {
  // schedules = _.sortBy(schedules, 'type');
  // schedules = _.sortBy(schedules, 'cinema_id');
  // schedules = _.sortBy(schedules, 'date');
  timSort.sort(schedules, timeCmp);
  timSort.sort(schedules, typeCmp);
  timSort.sort(schedules, cinemaCmp);
  timSort.sort(schedules, dateCmp);
  for (var i in schedules) {
    delete schedules[i]['cinema']
  }
  return schedules;
}

// Create endpoint for /api/movies/schedule for GET
exports.getMovieScheduleById = function (req, res) {
  Movie.getMovieScheduleById(req.headers.movie_id)
    .then(function (schedules) {
      schedules = parseSchedule(schedules);
      schedules = sortSchedule(schedules);
      res.json(schedules);
    }).catch(function (err) {
      console.log(err);
  })
};

// Create endpoint /api/movies/id for GET
exports.getMoviesById = function (req, res) {
  // Use the Client model to find all clients
  Movie.find({where: {id: req.headers.id}}).then(function (movies) {
    res.json(movies);
  }).catch(function (err) {
    res.send(err);
  });
};

// Create endpoint /api/movies/productionYear for GET
exports.getMoviesByProductionYear = function (req, res) {
  // Use the Client model to find all clients
  Movie.find({where: {productionYear: req.headers.productionYear}})
    .then(function (movies) {
      res.json(movies);
    }).catch(function (err) {
    res.send(err);
  });
};
