from django.test import LiveServerTestCase
from selenium import webdriver


class AdminTest(LiveServerTestCase):
    fixtures = ['fixtures/one_user_logged_in.json']
    
    def setUp(self):
        self.browser = webdriver.PhantomJS()

        # add session cookie for logged-in user
        self.browser.add_cookie({u'domain': u'127.0.0.1', u'name': u'sessionid',
                                 u'value': u'en7bsoxribtozhk7gewvwld1ncvpubem',
                                 u'path': u'/', u'httponly': True, u'secure': False})

    def tearDown(self):
        self.browser.quit()

    def test_can_access_admin_site(self):
        self.browser.get(self.live_server_url + '/admin/')
        # check 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)