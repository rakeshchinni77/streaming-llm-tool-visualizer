from app.services.tool_engine import ToolEngine
from app.tools.calculator import CalculatorTool
from app.tools.current_time import CurrentTimeTool


def test_calculator_tool_returns_expected_result() -> None:
    result = CalculatorTool().calculate("50 * 12")

    assert result == "600"


def test_current_time_tool_returns_utc_payload() -> None:
    result = CurrentTimeTool().get_current_time("UTC")

    assert result["timezone"] == "UTC"
    assert "current_time" in result


def test_tool_engine_returns_structured_error_for_unknown_tool() -> None:
    result = ToolEngine().execute("missing_tool", {})

    assert result["success"] is False
    assert "error" in result
