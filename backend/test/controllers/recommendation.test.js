var server = require('../../server.js');
var request = require('supertest');
var should = require('should');
var movie = require('../../models/movie.js');
var user = require('../../models/user.js');
var recommendation = require('../../models/recommendation');

function getObjects(obj, key, val) {
  var objects = [];
  for (var i in obj) {
    if (!obj.hasOwnProperty(i)) {
      continue;
    }
    if (typeof obj[i] == 'object') {
      objects = objects.concat(getObjects(obj[i], key, val));
    } else
    if (i === key && obj[i] === val || i === key && val === '') { //
      objects.push(obj);
    } else if (obj[i] === val && key === ''){
      if (objects.lastIndexOf(obj) === -1){
        objects.push(obj);
      }
    }
  }
  return objects;
}

describe('Bookmark controller test', function () {
  before(function (done) {
    movie.bulkCreate([
      {movie_id: 'test000001', title: 'test1: here StUpId ABcdE'},
      {movie_id: 'test000002', title: 'test2: testmoviename LK'},
      {movie_id: 'test000003', title: 'test3: here'},
      {movie_id: 'test000004', title: 'test dummy movie1'},
      {movie_id: 'test000005', title: 'test dummy movie2'}
    ]).then(function () {
      var password = user.getHashedPassword('pass');

      user.create({
        email: 'testemailmovietest',
        username: 'testusername',
        password: password
      }).then(function (users) {
        recommendation.bulkCreate([
          {user_id: users.id, movie_id: 'test000001', score: 1.3},
          {user_id: users.id, movie_id: 'test000002', score: 2.4},
          {user_id: users.id, movie_id: 'test000003', score: 4.7}
        ])
          .then(function () {
            done();
          })
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
            done();
          });
      });
  });

  it('should get all recommendations from the db', function (done) {
    request(server)
      .get('/api/recommendations')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        res.body.length.should.equal(3);
        done();
      });
  });

});
