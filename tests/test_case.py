import unittest
from main import app


class HealthApiTestCase(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()
        self.app.testing = True

    def test_health_route(self):

        response = self.app.get('/health')


        self.assertEqual(response.status_code, 200)

        response_json = response.get_json()
        self.assertEqual(response_json["message"], "Server Health : Running")

class UiApiTestCase(unittest.TestCase):


    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

