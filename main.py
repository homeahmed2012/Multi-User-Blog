import os
import time
import jinja2
import webapp2
from sec import *
from helper import *
from entities import *
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render(self, template, **kw):
        t = jinja_env.get_template(template)
        self.write(t.render(kw))


class MainHandler(Handler):  # to handle the Home page
    def get(self):
        blogs = mostRecentBlogs()
        h = self.request.cookies.get('user_id')
        text = ""
        if h and check_secure_val(h):
            user_name = User.get_by_id(long(check_secure_val(h))).user_name
            text = "welcome, %s!" % user_name
        self.render("main_page.html",
                    blogs=blogs,
                    text=text)


class SignHandler(Handler):  # to handle the Signup form
    def get(self):
        self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        repass = self.request.get("verify")
        email = self.request.get("email")
        res = validate(username,
                       password,
                       repass,
                       email)
        if res[0]:
            hash_pass = make_pw_hash(username, password)
            if email:
                u = User(user_name=username, password=hash_pass, email=email)
            else:
                u = User(user_name=username, password=hash_pass)
            u.put()
            sec_cookie = make_secure_val(str(u.key().id()))
            self.response.headers.add_header('Set-Cookie',
                                             'user_id=%s; Path=/' % sec_cookie)
            self.redirect('/')
        else:
            self.render("signup.html",
                        text1=res[1],
                        text2=res[2],
                        text3=res[3],
                        text4=res[4],
                        vus=username,
                        vem=email)


class WelHandler(Handler):  # to handle the welcome page
    def get(self):
        h = self.request.cookies.get('user_id')
        if h and check_secure_val(h):
            text = "welcome, %s!"
            user_name = User.get_by_id(long(check_secure_val(h))).user_name
            self.write(text % user_name)
        else:
            self.redirect('/signup')


class LogHandler(Handler):  # to handle the Login page
    def get(self):
        self.render("login.html")

    def post(self):
        us = self.request.get("username")
        ps = self.request.get("password")
        u = db.GqlQuery("SELECT * FROM User WHERE user_name = :1"
                        , us).get()
        new_hash = ""
        if u:
            new_hash = make_pw_hash(us, ps, u.password.split('|')[1])
        if u and u.password == new_hash:
            sec_cookie = make_secure_val(str(u.key().id()))
            self.response.headers.add_header('Set-Cookie',
                                             'user_id=%s; Path=/' % sec_cookie)
            self.redirect('/')
        else:
            text = 'Invalid login'
            self.render("login.html",
                        text2=text)


class LogOutHandler(Handler):  # to handle the Logout
    def get(self):
        self.response.headers.add_header('Set-Cookie',
                                         'user_id=; Path=/')
        self.redirect('/')


class Fpost(Handler):  # to handle the finished blog page
    def get(self, post_id):
        blogs = Blog.get_by_id(long(post_id))
        self.render("fisish_blog.html"
                    , blogs=blogs)

    def post(self):
        pass


class NewPost(Handler):  # to handle the Add new post page
    def get(self):
        h = self.request.cookies.get('user_id')
        if h and check_secure_val(h):
            self.render("new_blog.html")
        else:
            self.redirect('/login')

    def post(self):
        h = self.request.cookies.get('user_id')
        sub = self.request.get('subject')
        bod = self.request.get('content')
        a = Blog(subject=sub,
                 body=bod,
                 user_id=long(h.split('|')[0]),
                 like=0)
        a.put()
        self.redirect('/blog/' + str(a.key().id()))


class CommentHandler(Handler):  # to handle adding comments
    def get(self, blog_id):
        blog = getBlog(blog_id)
        self.render("commentBlog.html",
                    blog=blog)

    def post(self, blog_id):
        c = Comment(content=self.request.get('new_comment'),
                    blog_id=long(blog_id))
        c.put()
        self.get(blog_id)


class EditHandler(Handler):  # to handle editing a blog
    def get(self, blog_id):
        h = self.request.cookies.get('user_id')
        if h and check_secure_val(h):
            cookie_user_id = long(h[0])
            blog = getBlog(blog_id)[0]
            if blog.user_id == cookie_user_id:
                self.render("editBlog",
                            blog=blog)
            else:
                self.write("error, you can edit your blogs only.")
                time.sleep(2)
                self.redirect('/')
        else:
            self.redirect('/login')

    def post(self, blog_id):
        blog = getBlog(blog_id)
        blog.body = self.request.get('content')
        blog.put()
        self.redirect('/')


class LikeHandler(Handler):  # to handle like a blog
    def get(self, blog_id):
        h = self.request.cookies.get('user_id')
        if h and check_secure_val(h):
            blog = getBlog(blog_id)[0]
            blog.like += 1
            blog.put()
            self.redirect('/')
        else:
            self.redirect('/login')


class DelHandler(Handler):  # to handle deleting blog
    def get(self, blog_id):
        h = self.request.cookies.get('user_id')
        if h and check_secure_val(h):
            blog = getBlog(blog_id)[0]
            blog.delete()
            self.redirect('/')
        else:
            self.redirect('/login')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignHandler),
    ('/login', LogHandler),
    ('/logout', LogOutHandler),
    ('/welcome', WelHandler),
    ('/blog/(\d+)', Fpost),
    ('/newpost', NewPost),
    ('/comment/(\d+)', CommentHandler),
    ('/edit/(\d+)', EditHandler),
    ('/like/(\d+)', LikeHandler),
    ('/del/(\d+)', DelHandler)
], debug=True)
