var server = require('../../server.js');
var request = require('supertest');
var should = require('should');
var movie = require('../../models/movie.js');
var cinema = require('../../models/cinema.js');
var showing = require('../../models/showing.js');
var user = require('../../models/user.js');
var crypto = require('crypto');

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

describe('Showing controller test', function () {
  before(function (done) {
    movie.bulkCreate([
      {movie_id: 'test000001', title: 'test1: here StUpId ABcdE'},
      {movie_id: 'test000002', title: 'test2: testmoviename LK'},
      {movie_id: 'test000003', title: 'test3: here'},
      {movie_id: 'test000004', title: 'test dummy movie1'},
      {movie_id: 'test000005', title: 'test dummy movie2'}
    ]).then(function () {
      var password = 'pass';
      var shasum = crypto.createHash('sha1');
      shasum.update(password);
      password = shasum.digest('hex');

      user.create({
        email: 'testemailmovietest',
        username: 'testusername',
        password: password
      }).then(function () {
        cinema.bulkCreate([
          {cinema_id: 1, cinema_name: 'testcinema1', provider: 'pigeon', url: 'pigeon.com'},
          {cinema_id: 2, cinema_name: 'testcinema2', provider: 'pigeon1', url: 'pigeo1n.com'}
        ]).then(function () {
          showing.bulkCreate([
            {cinema_id: 1, movie_id: 'test000001', type: 'type1', schedule: '2017-03-03 12:51:11+08'},
            {cinema_id: 1, movie_id: 'test000002', type: 'type2', schedule: '2017-03-03 13:13:11+08'},
            {cinema_id: 2, movie_id: 'test000001', type: 'type3', schedule: '2017-03-03 14:22:11+08'},
            {cinema_id: 2, movie_id: 'test000001', type: 'type4', schedule: '2017-03-03 15:22:11+08'},
            {cinema_id: 2, movie_id: 'test000003', type: 'type1', schedule: '2017-03-03 16:00:11+08'},
            {cinema_id: 2, movie_id: 'test000004', type: 'type2', schedule: '2017-03-03 17:44:11+08'}
          ])
        });
        done();
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

  it('should get a movie from the db by its title', function (done) {
    request(server)
      .get('/api/showing')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .set('cinema_id', '1')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        var data = res.body.raw;
        getObjects(data, 'movie_id', 'test000001').should.not.equal([]);
        getObjects(data, 'movie_id', 'test000001').should.not.equal([]);
      });

    request(server)
      .get('/api/showing')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .set('cinema_id', '2')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        var data = res.body.raw;
        getObjects(data, 'movie_id', 'test000001').should.not.equal([]);
        getObjects(data, 'movie_id', 'test000003').should.not.equal([]);
        getObjects(data, 'movie_id', 'test000004').should.not.equal([]);
        done();
      });
  });

  it('should get all now showing movie', function (done) {
    request(server)
      .get('/api/showing/all')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .set('cinema_id', '2')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        var data = res.body;
        data.length.should.equal(4);
        done();
      });
  });
});
