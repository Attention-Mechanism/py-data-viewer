from typing import Any, NamedTuple, Optional, List
import argparse, re, inspect, ast


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


class TreeNode:
    """Represents a node in the object tree visualization"""

    def __init__(self, path: str, value: Any, is_leaf: bool = False):
        self.path = path
        self.value = value
        self.is_leaf = is_leaf
        self.children: List["TreeNode"] = []

    def add_child(self, child: "TreeNode") -> None:
        self.children.append(child)


class DataViewer:
    def __init__(
        self,
        data: Any,
        indent_size: int = 2,
        colorize: bool = True,
        var_name: Optional[str] = None,
        tree_view: bool = False,
    ):
        self.data = data
        self.indent_size = indent_size
        self.colorize = colorize
        self.var_name = var_name or self._uselessly_detect_variable_name()
        self.tree_view = tree_view
        self.tree_root = None

    def _uselessly_detect_variable_name(self):
        """
        Attempt to detect the variable name from the call stack.
        This is a best effort and may not always work (if at all)!
        """
        try:
            # Get the frame where DataViewer was instantiated
            current_frame = inspect.currentframe()
            frame = current_frame.f_back if current_frame else None

            # Get the source code of the line where DataViewer was called
            context_lines = inspect.getframeinfo(frame).code_context if frame else None
            if not context_lines:
                return "data"

            # The line where DataViewer was instantiated
            call_line = context_lines[0].strip()

            # Parse the line with ast to find the argument
            # This handles cases like: DataViewer(response).explore()
            try:
                tree = ast.parse(call_line)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and call_line.find("DataViewer") >= 0:
                        if node.args:
                            arg_node = node.args[0]
                            if isinstance(arg_node, ast.Name):
                                return arg_node.id
            except SyntaxError:
                # If we can't parse the line, try a regex approach
                pass

            # Fallback to regex pattern matching
            # Look for DataViewer(variable_name) pattern
            match = re.search(r"DataViewer\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)", call_line)
            if match:
                return match.group(1)

        except Exception:
            # Silently fail bc why not and then use default 🤪
            pass

        return "data"  # yup default fallback

    def explore(self, prefix=None):
        """
        Recursively explore the data structure and print how to access each value

        Args:
            prefix: Optional custom prefix for the variable name.
                   If None, will use the "detected" variable name.
        """
        prefix = prefix or self.var_name

        if self.tree_view:
            # Build the tree structure first
            self.tree_root = TreeNode(prefix, self.data)
            self._build_tree(self.data, prefix, self.tree_root)
            # Then print the tree
            self._print_tree(self.tree_root)
        else:
            # Original flat exploration
            self._explore(self.data, prefix, depth=0)

        return self  # Return self to allow method chaining

    def _build_tree(self, data: Any, path: str, parent_node: TreeNode, depth: int = 0) -> None:
        """Build a tree representation of the data structure"""
        if isinstance(data, dict):
            for key, value in data.items():
                key_repr = f"['{key}']"
                path_str = f"{path}{key_repr}"
                child_node = TreeNode(path_str, value)
                parent_node.add_child(child_node)
                self._build_tree(value, path_str, child_node, depth + 1)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                index_repr = f"[{index}]"
                path_str = f"{path}{index_repr}"
                child_node = TreeNode(path_str, value)
                parent_node.add_child(child_node)
                self._build_tree(value, path_str, child_node, depth + 1)
        elif hasattr(data, "__dict__"):  # For objects with attributes
            for attr, value in vars(data).items():
                attr_repr = f".{attr}"
                path_str = f"{path}{attr_repr}"
                child_node = TreeNode(path_str, value)
                parent_node.add_child(child_node)
                self._build_tree(value, path_str, child_node, depth + 1)
        else:
            # 🍃 It's a leaf node, mark it as such!! EASIER!!
            parent_node.is_leaf = True

    def _print_tree(
        self, node: TreeNode, prefix: str = "", is_last: bool = True, depth: int = 0
    ) -> None:
        """Print the tree structure with extracted values"""
        # For the root node, just print name iguess
        if depth == 0:
            print(f"{node.path}")
            # Print children with proper indentation this time!!
            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                self._print_tree(child, "", is_last_child, depth + 1)
            return

        # Determine the branch character
        branch = "└── " if is_last else "├── "

        # For non-root nodes
        if node.is_leaf:
            node_value = repr(node.value)
        elif isinstance(node.value, (dict, list, tuple, set)):
            node_value = f"{type(node.value).__name__} with {len(node.value)} items"
        elif hasattr(node.value, "__dict__"):
            node_value = f"Object of type {type(node.value).__name__}"
        else:
            node_value = repr(node.value)

        if self.colorize:
            colored_path = Colors.colorize_path(node.path)
            print(f"{prefix}{branch}{colored_path} = {node_value}")
        else:
            print(f"{prefix}{branch}{node.path} = {node_value}")

        # Calculate the new prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Print children nodes
        for i, child in enumerate(node.children):
            is_last_child = (
                # Use node! Node captures the whole tree
                i
                == len(node.children) - 1
            )
            self._print_tree(child, new_prefix, is_last_child, depth + 1)

    def _explore(self, data: Any, path: str, depth: int = 0):
        indent = " " * (depth * self.indent_size)

        if isinstance(data, dict):
            for key, value in data.items():
                key_repr = f"['{key}']"
                path_str = f"{path}{key_repr}"
                if self.colorize:
                    colored_path = Colors.colorize_path(path_str)
                    print(f"{indent}{colored_path} = {repr(value)}")
                else:
                    print(f"{indent}{path_str} = {repr(value)}")
                self._explore(value, path_str, depth + 1)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                index_repr = f"[{index}]"
                path_str = f"{path}{index_repr}"
                if self.colorize:
                    colored_path = Colors.colorize_path(path_str)
                    print(f"{indent}{colored_path} = {repr(value)}")
                else:
                    print(f"{indent}{path_str} = {repr(value)}")
                self._explore(value, path_str, depth + 1)
        elif hasattr(data, "__dict__"):  # For objects with attributes
            for attr, value in vars(data).items():
                attr_repr = f".{attr}"
                path_str = f"{path}{attr_repr}"
                if self.colorize:
                    colored_path = Colors.colorize_path(path_str)
                    print(f"{indent}{colored_path} = {repr(value)}")
                else:
                    print(f"{indent}{path_str} = {repr(value)}")
                self._explore(value, path_str, depth + 1)
        else:
            # Base case: primitive value bc yes
            pass


def vprint(
    data: Any,
    var_name: Optional[str] = None,
    colorize: bool = True,
    tree_view: bool = True,
    indent_size: int = 2,
):
    """
    Shorthand for printing the exploration of a data structure using DataViewer.

    Args:
        data (Any): The data structure to explore.
        var_name (Optional[str], optional): Variable name for the root of the data structure. Defaults to None.
        colorize (bool, optional): Enable/disable colorized output. Defaults to True.
        tree_view (bool, optional): Display as a tree structure. Defaults to True.
        indent_size (int, optional): (Only if tree_view=False) Indentation size for nested levels. Defaults to 2.
    """
    explorer = DataViewer(
        data,
        indent_size=indent_size,
        colorize=colorize,
        var_name=var_name or "data",
        tree_view=tree_view,
    )
    explorer.explore()


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
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation size for nested levels",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colorized output",
    )
    parser.add_argument(
        "--tree",
        action="store_true",
        help="Display as a tree structure",
    )
    args = parser.parse_args()

    # Get the selected sample data
    sample_data = get_sample_data(args.type)

    print(f"\n--- Exploring {args.type} data structure ---\n")

    # Create navigator with selected data and explore it
    navigator = DataViewer(
        sample_data, indent_size=args.indent, colorize=not args.no_color, tree_view=args.tree
    )
    navigator.explore()

    print("\nUsage examples:")
    print(f"  python value_navigator.py --type dict     # Explore a dictionary")
    print(f"  python value_navigator.py --type list     # Explore a list")
    print(f"  python value_navigator.py --type object   # Explore an object")
    print(f"  python value_navigator.py --type namedtuple  # Explore a namedtuple")
    print(f"  python value_navigator.py --type complex  # Explore a complex mixed structure")
    print(f"  python value_navigator.py --indent 4      # Use 4 spaces for indentation")
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
