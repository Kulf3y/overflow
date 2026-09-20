import unittest

from fastapi.testclient import TestClient

from overflow.gateway import app

client = TestClient(app)


class StreamingTests(unittest.TestCase):
    def test_stream_returns_sse(self):
        res = client.post("/v1/chat/stream", json={"text": "Hello streaming world"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("data:", res.text)
        self.assertIn("[DONE]", res.text)


if __name__ == "__main__":
    unittest.main()
