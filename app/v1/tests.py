from fastapi.testclient import TestClient
from run import app
import unittest

INPUT = {"data": "example data"}

class ApiUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_health(self):
        with TestClient(app) as client:
            response = client.get(f"/health")
            self.assertEqual(response.status_code, 200)

    def test_predict(self):
        with TestClient(app) as client:
            response = client.post(f"/predict", json=INPUT)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(
                any([
                    response.json() == {"prediction": 1},
                    response.json() == {"prediction": 0},
                ])
            )


# test_health()

# import json
# import unittest
# import requests


# URL = "http://localhost"
# PORT = "8080"

# INPUT = {"data": "example data"}


# class ApiUnitTest(unittest.TestCase):
#     def setUp(self) -> None:
#         global URL
#         global PORT
#         self.url = f"{URL}:{PORT}"
#         if not self.url.startswith("http://") or self.url.startswith("https://"):
#             self.url = "http://" + self.url

#         if self.url.endswith("/"):
#             self.url = self.url[:-1]

#     def test_health(self):
#         res = requests.get(f"{self.url}/health")
#         self.assertTrue(res.status_code == 200)

#     def test_predict(self):
#         res = requests.post(f"{self.url}/score", json=INPUT)
#         print(json.dumps({"status code": res.status_code, "output": res.text}, indent=2))
#         self.assertTrue(res.status_code == 200)
