var cinema = require('../../models/cinema');
var server = require('../../server.js');
var request = require('supertest');
var should = require('should');
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

describe('Cinema controller test', function () {
  before(function (done) {
    cinema.bulkCreate([
      {cinema_name: 'testcinema1', provider: 'pigeon', url: 'pigeon.com'},
      {cinema_name: 'testcinema2', provider: 'pigeon1', url: 'pigeo1n.com'},
      {cinema_name: 'testcinema3', provider: 'pigeon', url: 'pigeon.com'},
      {cinema_name: 'testcinema4', provider: 'pigeon2', url: 'pigeo2n.com'},
      {cinema_name: 'testcinema5', provider: 'pigeon', url: 'pigeo3n.com'}
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

  it('should get all cinema from the db', function (done) {
    request(server)
      .get('/api/cinemas')
      .set('Content-Type', 'application/x-www-form-urlencoded')
      .auth('testemailmovietest', 'pass')
      .set('Title', 'test1')
      .expect(200)
      .end(function (err, res) {
        res.status.should.equal(200);
        var data = res.body.raw;
        getObjects(data, 'cinema_name', 'testcinema1').should.not.equal([]);
        getObjects(data, 'cinema_name', 'testcinema2').should.not.equal([]);
        getObjects(data, 'cinema_name', 'testcinema3').should.not.equal([]);
        getObjects(data, 'cinema_name', 'testcinema4').should.not.equal([]);
        getObjects(data, 'cinema_name', 'testcinema5').should.not.equal([]);
        done();
      });
  });
});
