from py_data_viewer import vprint
from py_data_viewer.py_data_viewer import DataViewer
import io  # For capturing output
import sys  # For redirecting stdout


def test_explore_simple_dict():
    sample_dict = {"key1": "value1", "key2": 42}
    viewer = DataViewer(sample_dict, var_name="test_data", tree_view=False, colorize=False)

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to our StringIO object
    viewer.explore()
    sys.stdout = sys.__stdout__  # Restore stdout

    expected_output = """test_data['key1'] = 'value1'
                            test_data['key2'] = 42
                        """
    assert captured_output.getvalue() == expected_output


def test_vprint_simple_dict():
    """Test that vprint correctly displays a simple dictionary."""
    sample_dict = {"key1": "value1", "key2": 42}

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to our StringIO object

    # Call vprint with default arguments but disable colorize and tree_view for consistent testing
    vprint(sample_dict, var_name="test_data", colorize=False, tree_view=False)

    sys.stdout = sys.__stdout__  # Restore stdout

    expected_output = """test_data['key1'] = 'value1'
                            test_data['key2'] = 42
                        """
    assert captured_output.getvalue() == expected_output


def test_vprint_with_tree_view():
    """Test that vprint correctly displays a simple dictionary with tree view."""
    sample_dict = {"key1": "value1", "key2": 42}

    # Capture the output that would normally go to the console
    captured_output = io.StringIO()
    sys.stdout = captured_output  # Redirect stdout to our StringIO object

    # Call vprint with tree_view=True but disable colorize for consistent testing
    vprint(sample_dict, var_name="test_data", colorize=False, tree_view=True)

    sys.stdout = sys.__stdout__  # Restore stdout

    expected_output = """test_data
                            ├── test_data['key1'] = 'value1'
                            └── test_data['key2'] = 42
                        """
    assert captured_output.getvalue() == expected_output
