from fakeredis import FakeStrictRedis
import unittest
from starlette.testclient import TestClient

from taskman.main import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_hello_kashaf(self):
        response = self.client.get("/kashaf")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello Kashaf"})

    # def test_redirect_to_tasks(self):
    #     response = self.client.get("/")
    #     self.assertEqual(response.status_code, 307)
    #     self.assertEqual(response.headers["location"], "/tasks")

    # def test_get_tasks(self):
    #     response = self.client.get("/tasks")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json(), [])

    # def test_get_task(self):
    #     task_id = "123"
    #     response = self.client.get(f"/tasks/{task_id}")
    #     self.assertEqual(response.status_code, 404)

    def test_create_task(self):
        data = {"name": "New Task", "description": "Task description"}
        response = self.client.post("/tasks", json=data)
        self.assertEqual(response.status_code, 200)
        task_id = response.text
        self.assertTrue(task_id)


if __name__ == "__main__":
    unittest.main()


