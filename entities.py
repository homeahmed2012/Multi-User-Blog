from google.appengine.ext import db
from google.appengine.ext import ndb
"""
This file acts as an interface to datasotre
it contains the entities for blog, user, and comment
it contains also some helper functions to work with datastore
"""


class User(db.Model):
    user_name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty()

    @classmethod
    def checkUser(cls, username):
        """
        check if the user is already exist in the datasotre
        :return: True if the user is already exist False otherwise
        """
        result = db.GqlQuery("SELECT * FROM User WHERE user_name = :1",
                             username).get()
        return result is not None


class Blog(ndb.Model):
    subject = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    user_id = ndb.IntegerProperty(required=True)
    like = ndb.IntegerProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Comment(db.Model):
    content = db.StringProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    user_id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


def mostRecentBlogs():
    """
    this method return the 10 most recent blogs with their comments
    """
    blogs = ndb.gql("SELECT * FROM Blog ORDER BY created DESC LIMIT 10")
    result = []
    for b in blogs:
        blogId = b.key.id()
        comments = db.GqlQuery("SELECT * FROM Comment WHERE blog_id = :1"
                               " ORDER BY created DESC LIMIT 5", blogId)
        result.append((b, comments, len(b.like)))
    return result


def getBlog(blog_id):
    """
     return a tuple of the blog with specified id and it's comments 
    """
    b = Blog.get_by_id(long(blog_id))
    comments = db.GqlQuery("SELECT * FROM Comment WHERE blog_id = :1"
                           " ORDER BY created DESC", long(blog_id))
    return b, comments
