from django.test import TestCase

class TestLogin(TestCase):
    def test_profile_page(self):
        response = self.client.get('/app_users/another_login/')
        self.assertTemplateUsed(response, 'app_users/login.html')