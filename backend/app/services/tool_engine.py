from app.tools.calculator import CalculatorTool


class ToolEngine:
    def __init__(self) -> None:
        self.tools = {
            "calculator": CalculatorTool(),
        }

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        tool = self.tools[tool_name]
        if tool_name == "calculator":
            expression = arguments.get("expression")
            return tool.calculate(expression)

        raise ValueError(f"Tool execution not implemented for: {tool_name}")
