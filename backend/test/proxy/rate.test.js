var should = require('should');
var movie = require('../../models/movie.js');
var user = require('../../models/user.js');
var rate = require('../../models/history.js');
var rateProxy = require('../../proxy/rate');

describe('Rate proxy test', function () {
  beforeEach(function (done) {
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
      }).then(function () {
        done();
      });
    });
  });

  afterEach(function (done) {
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

  it('should post a rate, postRates', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      rateProxy.postRates(1.2, 'test000001', users.id)
        .then(function (rates) {
          rates.score.should.equal(1.2);
          rates.movie_id.should.equal('test000001');
          rates.user_id.should.equal(users.id);
          done();
        })
    })
  });

  it('should get all rate, postRates', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      rate.bulkCreate([
        {movie_id: 'test000001', user_id: users.id, score: 1.1},
        {movie_id: 'test000003', user_id: users.id, score: 4.6},
        {movie_id: 'test000005', user_id: users.id, score: 7.7},
      ])
        .then(function () {
          rateProxy.getAllRates(users.id)
            .then(function (rates) {
              rates.length.should.equal(3);
              rates[0].movie_id.should.equal('test000001');
              rates[1].movie_id.should.equal('test000003');
              rates[2].movie_id.should.equal('test000005');
              done();
            })
        });
    })
  });

  it('should get a rate, getSpecificRate', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      rate.bulkCreate([
        {movie_id: 'test000001', user_id: users.id, score: 1.1}
      ])
        .then(function () {
          rateProxy.getSpecificRate(users.id, 'test000001')
            .then(function (rates) {
              rates.dataValues.score.should.equal(1.1);
              done();
            })
        });
    })
  });

  it('should update a rate, updateRates', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      rate.bulkCreate([
        {movie_id: 'test000001', user_id: users.id, score: 1.1}
      ])
        .then(function () {
          rate.find({
            where: {
              movie_id: 'test000001'
            }
          })
            .then(function (rating) {
              rateProxy.updateRates(rating, 3.6)
                .then(function (rates) {
                  rates.dataValues.score.should.equal(3.6);
                  done();
                })
            });
        });
    })
  });
});
