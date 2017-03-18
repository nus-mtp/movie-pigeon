

module.exports.hasSchedule = function (movies) {
  for (var i in movies) {
    var schedule = movies[i].dataValues.showings;
    if (schedule.length == 0) {
      movies[i].dataValues.isShowing = false;
    } else {
      movies[i].dataValues.isShowing = true;
    }
    delete movies[i].dataValues.showings;
  }
  return movies;
};
