import browser


def tearDown():
    browser.close()


class AdminTest(browser.SignedInTest):
    def test_can_access_admin_site(self):
        browser.instance().get(self.live_server_url + '/admin/')
        # check 'Django administration' heading
        body = browser.instance().find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)