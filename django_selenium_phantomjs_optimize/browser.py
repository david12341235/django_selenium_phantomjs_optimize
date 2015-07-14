from django.test import LiveServerTestCase
from selenium import webdriver
import autofixture
from django.contrib.auth import hashers


browser = []


def instance():
    # other browsers can be set here, eg
    # webdriver.Firefox()
    # Firefox, however, requires you to load a page in the
    # domain before setting a cookie, with eg:
    # instance().get(self.live_server_url)
    if len(browser) < 1:
        browser.append(webdriver.PhantomJS())
    return browser[0]


def close():
    instance().quit()
    browser.pop(0)


class SignedInTest(LiveServerTestCase):
    def setUp(self):
        u = autofixture.create_one('auth.User', generate_fk=True,
                                   field_values={'password': hashers.make_password('password')})
        u.save()

        # add session cookie for logged-in user
        self.client.login(email=u.email, password='password')
        instance().add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        instance().delete_all_cookies()