from src.py_data_viewer.py_data_viewer import vprint
from tests.service import generate_mock_response
import io
import sys


def test_vprint_complex_structure():
    """Test that vprint correctly displays a complex mixed structure."""
    complex_data = generate_mock_response()

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to StringIO object

    # Test the vprint function with the complex data
    vprint(complex_data, var_name="complex_data", colorize=False)

    sys.stdout = sys.__stdout__  # Restore stdout

    actual_output = captured_output.getvalue()

    assert "complex_data" in actual_output
    assert "chat_message" in actual_output
    assert "inner_messages" in actual_output
    assert "ToolCallSummaryMessage" in actual_output
    assert "ToolCallRequestEvent" in actual_output
    assert "ToolCallExecutionEvent" in actual_output
