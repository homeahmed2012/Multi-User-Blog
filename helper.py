import re
from entities import *

"""
this file contains some helper methods to validate user information
"""

valid_us = "That&#39;s not a valid username."
valid_ps = "That wasn&#39;t a valid password."
valid_vp = "Your passwords didn&#39;t match."
valid_email = "That&#39;s not a valid email."

user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
pass_re = re.compile(r"^.{3,20}$")
email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def validate(username, password, repass, email):
    """
    check the validation of user informations
    :return: a tuple contains a boolean which 
    is True if the information is valid and False otherwise
    and 4 strings to render them in the signup form
    """
    b1 = user_re.match(username)
    b2 = pass_re.match(password)
    b3 = (password == repass)
    b4 = True if email else email_re.match(email)
    text1 = valid_us if not b1 else ""
    text2 = valid_ps if not b2 else ""
    text3 = valid_vp if not b3 else ""
    text4 = valid_email if not b4 else ""
    if checkUser(username):
        text1 = "That user already exists."
        b1 = False
        username = ""
    return (b1 and b2 and b3 and b4), text1, text2, text3, text4
