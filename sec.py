import random
import string
import hashlib
# import hmac

"""
this file contains the methods that hash the password and the cookies
"""


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    hash_result = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (hash_result, salt)


def valid_pw(name, pw, h):
    a = h.split('|')[1]
    return h == make_pw_hash(name, pw, a)

# ================================================================


def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    a = h.split('|')
    if a[1] == hash_str(a[0]):
        return a[0]
