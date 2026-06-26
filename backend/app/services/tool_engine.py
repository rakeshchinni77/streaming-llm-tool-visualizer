import logging
from typing import Any, Callable

from app.tools.calculator import CalculatorTool
from app.tools.current_time import CurrentTimeTool
from app.tools.knowledge_tool import KnowledgeTool

logger = logging.getLogger(__name__)


class ToolEngine:
    def __init__(self) -> None:
        self.calculator_tool = CalculatorTool()
        self.current_time_tool = CurrentTimeTool()
        self.knowledge_tool = KnowledgeTool()
        self.registry: dict[str, Callable[[dict], Any]] = {
            "calculator": self._run_calculator,
            "current_time": self._run_current_time,
            "knowledge_base": self._run_knowledge_base,
        }

    def _run_calculator(self, arguments: dict) -> Any:
        return self.calculator_tool.calculate(arguments.get("expression"))

    def _run_current_time(self, arguments: dict) -> Any:
        return self.current_time_tool.get_current_time(arguments.get("timezone", "UTC"))

    def _run_knowledge_base(self, arguments: dict) -> Any:
        return self.knowledge_tool.search_knowledge(arguments.get("query", ""))

    def execute(self, tool_name: str, arguments: dict) -> dict:
        if tool_name not in self.registry:
            return {
                "tool": tool_name,
                "success": False,
                "error": f"Unknown tool: {tool_name}",
            }

        try:
            result = self.registry[tool_name](arguments or {})
            return {
                "tool": tool_name,
                "success": True,
                "result": result,
            }
        except Exception as exc:
            logger.exception("Tool execution failed for %s", tool_name)
            return {
                "tool": tool_name,
                "success": False,
                "error": str(exc),
            }

    def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        return self.execute(tool_name, arguments)
