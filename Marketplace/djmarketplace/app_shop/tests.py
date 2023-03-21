from django.test import TestCase

class TestProductList(TestCase):

    def test_list(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

