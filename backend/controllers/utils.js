

module.exports.hasSchedule = function (movies) {
  for (var i in movies) {
    var schedule = movies[i].dataValues.showings;
    if (schedule.length == 0) {
      movies[i].dataValues.showings = false;
    } else {
      movies[i].dataValues.showings = true;
    }
  }
  return movies;
};
