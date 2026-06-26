import unittest

from app.services.tool_engine import ToolEngine


class KnowledgeToolTests(unittest.TestCase):
    def test_knowledge_tool_returns_atlas_answer(self) -> None:
        result = ToolEngine().execute_tool(
            "knowledge_base",
            {"query": "When will Atlas launch?"},
        )

        self.assertEqual(result["title"], "Atlas Project")
        self.assertIn("scheduled to launch in Q3", result["answer"])


if __name__ == "__main__":
    unittest.main()
