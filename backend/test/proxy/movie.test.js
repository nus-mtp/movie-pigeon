var server = require('../../server.js');
var should = require('should');
var movie = require('../../models/movie.js');
var user = require('../../models/user.js');
var cinema = require('../../models/cinema.js');
var showing = require('../../models/showing.js');
var movieProxy = require('../../proxy/movie');

var getObjects = function (obj, key, val) {
  var objects = [];
  for (var i in obj) {
    if (!obj.hasOwnProperty(i)) {
      continue;
    }
    if (typeof obj[i] == 'object') {
      objects = objects.concat(getObjects(obj[i], key, val));
    } else if (i === key && obj[i] === val || i === key && val === '') { //
      objects.push(obj);
    } else if (obj[i] === val && key === '') {
      if (objects.lastIndexOf(obj) === -1) {
        objects.push(obj);
      }
    }
  }
  return objects;
};

describe('Movie proxy test', function () {
  before(function (done) {
    movie.bulkCreate([
      {movie_id: 'test000001', title: 'test1: here StUpId ABcdE'},
      {movie_id: 'test000002', title: 'test2: testmoviename LK'},
      {movie_id: 'test000003', title: 'test3: here'},
      {movie_id: 'test000004', title: 'test dummy movie1'},
      {movie_id: 'test000005', title: 'test dummy movie2 pid'}
    ]).then(function () {
      var password = user.getHashedPassword('pass');

      user.create({
        email: 'testemailmovietest',
        username: 'testusername',
        password: password
      }).then(function () {
        cinema.bulkCreate([
          {cinema_id: 1, cinema_name: 'testcinema1', provider: 'pigeon', url: 'pigeon.com'}
        ]).then(function () {
          showing.bulkCreate([
            {cinema_id: 1, movie_id: 'test000001', type: 'type1', schedule: '2017-03-03 12:51:11+08'},
            {cinema_id: 1, movie_id: 'test000002', type: 'type2', schedule: '2017-03-03 13:13:11+08'}
          ]);
          done();
        });
      });
    });
  });

  after(function (done) {
    user.destroy({
      where: {
        email: 'testemailmovietest'
      }
    })
      .then(function () {
        movie.destroy({
          where: {
            movie_id: {$ilike: '%test%'}
          }
        })
          .then(function () {
            cinema.destroy({
              where: {
                cinema_name: {$ilike: '%testcinema%'}
              }
            })
              .then(function () {
                done();
              });
          });
      });
  });

  it('should get count from getMovieByTitleCount', function (done) {
    movieProxy.getMovieByTitleCount('dummy')
      .then(function (result) {
        result.should.equal(2);
        done();
      });
  });

  it('should get count from getMovieByTitleCount', function (done) {
    movieProxy.getMovieByTitleCount('stupid')
      .then(function (result) {
        result.should.equal(1);
        done();
      });
  });

  it('should get movie from getMovieByTitle', function (done) {
    movieProxy.getMovieByTitle(1, 'dummy')
      .then(function (result) {
        result.length.should.equal(2);
        result[0].dataValues.movie_id.should.equal('test000004');
        result[1].dataValues.movie_id.should.equal('test000005');
        done();
      })
  });

  it('should get movie from getShowingMovieByTitle', function (done) {
    movieProxy.getShowingMovieByTitle(1, 'here')
      .then(function (result) {
        result.length.should.equal(1);
        result[0].dataValues.movie_id.should.equal('test000001');
        done();
      })
  });

  it('should get movie from getMovieScheduleById', function (done) {
    movieProxy.getMovieScheduleById('test000001')
      .then(function (result) {
        result.dataValues.movie_id.should.equal('test000001');
        done();
      })
  });

  it('should get movie from getMovieScheduleById', function (done) {
    movieProxy.getMovieScheduleById('test000004')
      .then(function (result) {
        (result === null).should.equal(true);
        done();
      })
  });

});
