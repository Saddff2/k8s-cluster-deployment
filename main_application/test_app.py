import unittest
import requests

class TestFlaskApp(unittest.TestCase):
    def test_homepage(self):
        response = requests.get('http://localhost:5000') # Use container name
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()