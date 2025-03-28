import json
import unittest
import requests


URL = "http://localhost"
PORT = "8000"

INPUT = {"data": "example data"}


class ApiUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        global URL
        global PORT
        self.url = f"{URL}:{PORT}"
        if not self.url.startswith("http://") or self.url.startswith("https://"):
            self.url = "http://" + self.url

        if self.url.endswith("/"):
            self.url = self.url[:-1]

    def test_health(self):
        res = requests.get(f"{self.url}/health")
        self.assertTrue(res.status_code == 200)

    def test_predict(self):
        res = requests.post(f"{self.url}/predict", json=INPUT)
        print(json.dumps({"status code": res.status_code, "output": res.json()}, indent=2))
        self.assertTrue(res.status_code == 200)
