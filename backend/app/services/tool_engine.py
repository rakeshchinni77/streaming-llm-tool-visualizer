from app.tools.calculator import CalculatorTool
from app.tools.current_time import CurrentTimeTool


class ToolEngine:
    def __init__(self) -> None:
        self.tools = {
            "calculator": CalculatorTool(),
            "current_time": CurrentTimeTool(),
        }

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self.tools[tool_name]
        if tool_name == "calculator":
            expression = arguments.get("expression")
            return tool.calculate(expression)
        if tool_name == "current_time":
            tz = arguments.get("timezone", "UTC")
            return tool.get_current_time(tz)

        raise ValueError(f"Tool execution not implemented for: {tool_name}")
