from django.test import LiveServerTestCase
from selenium import webdriver
import autofixture
from django.contrib.auth import hashers


browser = []


def instance():
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

        # other browsers can be set here, eg
        # self.browser = webdriver.Firefox()

        # add session cookie for logged-in user
        self.client.login(email=u.email, password='password')
        instance().add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        instance().delete_all_cookies()