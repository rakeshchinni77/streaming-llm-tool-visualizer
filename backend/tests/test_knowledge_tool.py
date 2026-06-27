import unittest
from unittest.mock import patch

from app.services.tool_engine import ToolEngine


class KnowledgeToolTests(unittest.TestCase):
    @patch("app.tools.knowledge_tool.EmbeddingService.search")
    def test_knowledge_tool_returns_atlas_answer(self, mock_search) -> None:
        mock_search.return_value = {
            "title": "Atlas Project",
            "answer": "Atlas is scheduled to launch in Q3.",
        }

        result = ToolEngine().execute_tool(
            "knowledge_base",
            {"query": "When will Atlas launch?"},
        )

        self.assertEqual(result["result"]["title"], "Atlas Project")
        self.assertIn("Q3", result["result"]["answer"])


if __name__ == "__main__":
    unittest.main()
