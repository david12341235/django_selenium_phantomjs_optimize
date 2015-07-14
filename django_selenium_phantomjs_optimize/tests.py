from django.test import LiveServerTestCase
from selenium import webdriver
from django.contrib.auth import hashers
import autofixture


class AdminTest(LiveServerTestCase):
    def setUp(self):
        u = autofixture.create_one('auth.User', generate_fk=True,
                                   field_values={'password': hashers.make_password('password')})
        u.save()

        # add session cookie for logged-in user
        self.client.login(username=u.username, password='password')

        self.browser = webdriver.PhantomJS()
        self.browser.add_cookie({u'domain': u'localhost', u'name': u'sessionid',
                                 u'value': self.client.session.session_key,
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        self.browser.quit()

    def test_can_access_admin_site(self):
        self.browser.get(self.live_server_url + '/admin/')
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)