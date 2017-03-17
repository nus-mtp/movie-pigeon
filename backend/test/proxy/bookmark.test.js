var should = require('should');
var movie = require('../../models/movie.js');
var user = require('../../models/user.js');
var bookmark = require('../../models/bookmarks.js');
var bookmarkProxy = require('../../proxy/bookmark');

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

describe('Bookmark proxy test', function () {
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

  it('should post a bookmark, postBookmark', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      bookmarkProxy.postBookmark('test000001', users.id)
        .then(function () {
          bookmark.find({
            where: {
              user_id: users.id,
              movie_id: 'test000001'
            }
          })
            .then(function (result) {
              result.movie_id.should.equal('test000001');
              done();
            })
        })
    });
  });

  it('should post a bookmark, postBookmark', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      bookmarkProxy.postBookmark('test000001', users.id)
        .then(function () {
          bookmark.find({
            where: {
              user_id: users.id,
              movie_id: 'test000001'
            }
          })
            .then(function (result) {
              result.movie_id.should.equal('test000001');
              done();
            })
        })
    });
  });

  it('should get all bookmark, getAllBookmarks', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      bookmark.bulkCreate([
        {movie_id: 'test000001', user_id: users.id},
        {movie_id: 'test000003', user_id: users.id},
        {movie_id: 'test000004', user_id: users.id}
      ])
        .then(function () {
         bookmarkProxy.getAllBookmarks(users.id)
           .then(function (bookmarks) {
             bookmarks[0].movie_id.should.equal('test000001');
             bookmarks[1].movie_id.should.equal('test000003');
             bookmarks[2].movie_id.should.equal('test000004');
             done();
           })
        });
    })
  });

  it('should get specific bookmark, getSpecificBookmark', function (done) {
    user.find({
      where: {
        email: 'testemailmovietest'
      }
    }).then(function (users) {
      bookmark.bulkCreate([
        {movie_id: 'test000001', user_id: users.id},
        {movie_id: 'test000003', user_id: users.id},
        {movie_id: 'test000004', user_id: users.id}
      ])
        .then(function () {
          bookmarkProxy.getSpecificBookmark(users.id, 'test000003')
            .then(function (bookmarks) {
              (bookmarks === null).should.equal(false);
              bookmarks.movie_id.should.equal('test000003');
              done();
            })
        });
    })
  });

});
