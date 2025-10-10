"""
Integration test: mock FastAPI /rag/query endpoint and simulate Rasa action.
"""
import unittest
from fastapi.testclient import TestClient
from api.app.routes import router

class TestRagApiEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_rag_query_endpoint(self):
        payload = {"query": "Fjallraven Backpack specs", "top_k": 2, "use_hyde": False}
        response = self.client.post("/rag/query", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)

if __name__ == "__main__":
    unittest.main()
