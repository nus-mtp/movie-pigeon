var server = require('../../server.js');
var request = require('supertest');
var should = require('should');
var movie = require('../../models/movie.js');
var user = require('../../models/user.js');
var rate = require('../../models/rate.js');
var crypto = require('crypto');

describe('Rate controller test', function () {
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
            done();
          });
      });
  });

  it('should post a rate to the db', function (done) {
    request(server)
      .post('/api/movies/title')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .send('movie_id', 'test000001')
      .send('score', '4.5')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        res.body.status.should.equal('success');
        res.body.message.should.equal('Ratings Posted!');
        user.find({
          where: {
            email: 'testemailmovietest'
          }
        })
          .then(function (users) {
            rate.find({
              where: {
                movie_id: 'test000001',
                user_id: users.id
              }
            })
              .then(function (rating) {
                rating.score.should.equal(4.5);
              });
          });
        done();
      });
  });
});
