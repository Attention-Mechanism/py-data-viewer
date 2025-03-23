from typing import Any, NamedTuple, Optional, List
import argparse, re, inspect, ast
from .file_output import file_output
from .types import TreeNode, DataViewer


class Colors:
    # Different shades of blue from lightest to darkest
    BLUES = [
        "\033[38;5;81m",  # Sky blue
        "\033[38;5;75m",  # Medium blue
        "\033[38;5;69m",  # Deep blue
        "\033[38;5;25m",  # Dark blue
    ]
    RESET = "\033[0m"  # Reset to default color

    @classmethod
    def get_blue(cls, depth):
        """Get a blue shade based on depth (♻️ cycles if too deep)"""
        return cls.BLUES[depth % len(cls.BLUES)]

    @classmethod
    def colorize_path(cls, path_str):
        """
        Colorize different parts of the access path using blue shades
        Each component gets progressively darker blue. 🌊
        """
        # Split the path into components
        components = []

        # Match the variable name first
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)(.*)", path_str)
        if match:
            var_name = match.group(1)
            components.append(var_name)
            remaining = match.group(2)
        else:
            return path_str  # No variable name found

        # Find all accessors (dict keys, list indices, attributes)
        accessors = []

        # Process all dictionary keys ['key']
        dict_keys = re.findall(r"\['([^']+)'\]", remaining)
        for key in dict_keys:
            accessors.append(f"['{key}']")

        # Process all list indices [0]
        list_indices = re.findall(r"\[(\d+)\]", remaining)
        for idx in list_indices:
            accessors.append(f"[{idx}]")

        # Process all object attributes .attr
        attributes = re.findall(r"\.([a-zA-Z_][a-zA-Z0-9_]*)", remaining)
        for attr in attributes:
            accessors.append(f".{attr}")

        # Build the path with ✨colors✨
        colored_parts = [f"{cls.get_blue(0)}{components[0]}{cls.RESET}"]

        # Extract accessors in order from the original path
        ordered_accessors = []
        cursor = len(components[0])

        while cursor < len(path_str):
            # Check for dictionary key
            if path_str[cursor:].startswith("['"):
                end = path_str.find("']", cursor) + 2
                if end > cursor:
                    ordered_accessors.append(path_str[cursor:end])
                    cursor = end
                    continue

            # Check for list index
            if path_str[cursor:].startswith("["):
                end = path_str.find("]", cursor) + 1
                if end > cursor:
                    ordered_accessors.append(path_str[cursor:end])
                    cursor = end
                    continue

            # Check for attribute
            if path_str[cursor:].startswith("."):
                match = re.match(r"\.([a-zA-Z_][a-zA-Z0-9_]*)", path_str[cursor:])
                if match:
                    attr = match.group(1)
                    ordered_accessors.append(f".{attr}")
                    cursor += len(f".{attr}")
                    continue

            # If we got here lol, just advance one character
            cursor += 1

        # Apply ✨colors✨ to the ordered accessors
        for i, accessor in enumerate(ordered_accessors):
            color_idx = i + 1  # Start from 1 since 0 is for the variable name
            colored_parts.append(f"{cls.get_blue(color_idx)}{accessor}{cls.RESET}")

        return "".join(colored_parts)


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
