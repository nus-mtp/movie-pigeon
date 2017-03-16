var server = require('../../server.js');
var should = require('should');
var user = require('../../models/user.js');
var userProxy = require('../../proxy/user');

describe('User proxy test', function () {
  before(function (done) {
    var password = user.getHashedPassword('pass');
    user.create({
      email: 'testemail',
      username: 'testusername',
      password: password
    })
      .then(function () {
        done();
      });
  });

  after(function (done) {
    user.destroy({
      where: {
        email: 'testemail'
      }
    })
      .then(function () {
        done();
      });
  });

  it('should add a user to the db', function (done) {
    userProxy.saveUser('123@321345.abc', 'testname', 'testpassword')
      .then(function () {
        user.find({where: {username: 'testname'}})
          .then(function (users) {
            users.validPassword('testpassword').should.equal(true);
            users.destroy();
            done();
          })
      });
  });

  it('should update username', function (done) {
    user.find({
      where: {
        email: 'testemail'
      }
    }).then(function (users) {
      userProxy.updateUserUsername(users, 'newname')
        .then(function (updated) {
          updated.username.should.equal('newname');
          done();
        });
    })
  });

  it('should update password', function (done) {
    user.find({
      where: {
        email: 'testemail'
      }
    }).then(function (users) {
      userProxy.updateUserPassword(users, 'newpass')
        .then(function (updated) {
          updated.validPassword('newpass').should.equal(true);
          done();
        });
    })
  });
});
