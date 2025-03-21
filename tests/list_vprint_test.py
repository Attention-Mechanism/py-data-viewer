from src.py_data_viewer import vprint
import io  # For capturing output
import sys  # For redirecting stdout


def test_vprint_list_tree_view():
    """Test that vprint correctly displays a list with tree view."""
    sample_list = ["first item", ["nested", "list"], 42]

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to our StringIO object

    vprint(sample_list, var_name="test_list", colorize=False)

    sys.stdout = sys.__stdout__  # Restore stdout

    expected_output = """test_list
├── test_list[0] = 'first item'
├── test_list[1] = list with 2 items
│   ├── test_list[1][0] = 'nested'
│   └── test_list[1][1] = 'list'
└── test_list[2] = 42
"""
    assert captured_output.getvalue() == expected_output
