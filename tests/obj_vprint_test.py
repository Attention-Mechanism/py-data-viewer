from py_data_viewer import vprint
from py_data_viewer.py_data_viewer import ExampleData
import io  # For capturing output
import sys  # For redirecting stdout
import re  # For regex replacement


def test_vprint_object_tree_view():
    """Test that vprint correctly displays an object with tree view."""
    sample_obj = ExampleData()

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to our StringIO object

    vprint(sample_obj, var_name="test_obj", colorize=False)

    sys.stdout = sys.__stdout__  # Restore stdout

    expected_output = """test_obj
├── test_obj.name = 'Example Object'
├── test_obj.nested = Object of type NestedData
│   ├── test_obj.nested.attribute = 'nested value'
│   └── test_obj.nested.flag = True
└── test_obj.values = list with 3 items
    ├── test_obj.values[0] = 1
    ├── test_obj.values[1] = 2
    └── test_obj.values[2] = 3
"""
    assert captured_output.getvalue() == expected_output
