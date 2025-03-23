from typing import Any, NamedTuple, Optional, List
import argparse
from .file_output import file_output
from .types import DataViewer


def vprint(
    data: Any,
    var_name: Optional[str] = None,
    output: Optional[str] = None,
    colorize: bool = True,
):
    """
    Shorthand for printing the exploration of a data structure using DataViewer.

    Args:
        data (Any): The data structure to explore.
        var_name (Optional[str], optional): Variable name for the root of the data structure. Defaults to None.
        output_file (Optional[str], optional): File path to save the output. If provided, writes the output to the file.
        colorize (bool, optional): Enable/disable colorized output. Defaults to True.
    """
    explorer = DataViewer(
        data,
        var_name=var_name or "data",
        colorize=colorize,
    )

    # Print to terminal
    explorer.explore()

    # Write to file if output_file is provided
    if output:
        file_output(data, output, var_name=var_name)


# Example data structures
class ExampleData:
    def __init__(self):
        self.name = "Example Object"
        self.nested = NestedData()
        self.values = [1, 2, 3]


class NestedData:
    def __init__(self):
        self.attribute = "nested value"
        self.flag = True


class RequestUsage(NamedTuple):
    prompt_tokens: int
    completion_tokens: int


# Sample data structures for testing
def get_sample_data(data_type):
    samples = {
        "dict": {
            "key": "value",
            "nested_dict": {"inner_key": "inner_value"},
        },
        "list": [
            "first item",
            ["nested", "list", "items"],
            42,
        ],
        "object": ExampleData(),
        "namedtuple": RequestUsage(prompt_tokens=7, completion_tokens=248),
        "complex": {
            "string": "text value",
            "number": 42,
            "boolean": True,
            "none_value": None,
            "list": [1, 2, [3, 4]],
            "dict": {"key": "value"},
            "object": ExampleData(),
            "tuple": RequestUsage(prompt_tokens=10, completion_tokens=300),
        },
    }

    return samples.get(data_type, samples["dict"])


if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(
        description="Explore and navigate through different data structures"
    )
    parser.add_argument(
        "--type",
        choices=["dict", "list", "object", "namedtuple", "complex"],
        default="dict",
        help="Type of data structure to explore",
    )

    # TODO: REMOVE
    # parser.add_argument(
    #     "--indent",
    #     type=int,
    #     default=2,
    #     help="Indentation size for nested levels",
    # )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colorized output",
    )

    # TODO: REMOVE
    # parser.add_argument(
    #     "--tree",
    #     action="store_true",
    #     help="Display as a tree structure",
    # )

    args = parser.parse_args()

    # Get the selected sample data
    sample_data = get_sample_data(args.type)

    print(f"\n--- Exploring {args.type} data structure ---\n")

    # Create navigator with selected data and explore it
    navigator = DataViewer(sample_data, colorize=not args.no_color)
    navigator.explore()

    print("\nUsage examples:")
    print(f"  python value_navigator.py --type dict     # Explore a dictionary")
    print(f"  python value_navigator.py --type list     # Explore a list")
    print(f"  python value_navigator.py --type object   # Explore an object")
    print(f"  python value_navigator.py --type namedtuple  # Explore a namedtuple")
    print(f"  python value_navigator.py --type complex  # Explore a complex mixed structure")
    # TODO: REMOVE
    # print(f"  python value_navigator.py --indent 4      # Use 4 spaces for indentation")
    print(f"  python value_navigator.py --no-color      # Disable colored output")

    print("\nExample with automatically detected variable name:")
    example_data = {"key": "value"}
    DataViewer(example_data).explore()  # Should detect "example_data" but no and thats okay

    print("\nExample with explicit variable name:")
    data = {"key": "value"}
    DataViewer(data, var_name="custom_name").explore()

    # Example with tree view
    print("\nExample with tree view:")
    complex_data = get_sample_data("complex")
    vprint(complex_data, var_name="complex_data")
