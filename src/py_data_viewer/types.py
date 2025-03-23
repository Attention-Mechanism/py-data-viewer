import re
from typing import Any, List


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
        colorize: bool = True,
        var_name: str = "data",
    ):
        self.data = data
        self.colorize = colorize
        self.var_name = var_name
        self.tree_root = None

    def explore(self):
        """Recursively explore the data structure and print how to access each value"""
        self.tree_root = TreeNode(self.var_name, self.data)
        self._build_tree(self.data, self.var_name, self.tree_root)
        self._print_tree(self.tree_root)

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
        elif hasattr(data, "__dict__"):
            for attr, value in vars(data).items():
                attr_repr = f".{attr}"
                path_str = f"{path}{attr_repr}"
                child_node = TreeNode(path_str, value)
                parent_node.add_child(child_node)
                self._build_tree(value, path_str, child_node, depth + 1)
        else:
            parent_node.is_leaf = True

    def _print_tree(
        self, node: TreeNode, prefix: str = "", is_last: bool = True, depth: int = 0
    ) -> None:
        """Print the tree structure with extracted values"""
        if depth == 0:
            print(f"{node.path}")
            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                self._print_tree(child, "", is_last_child, depth + 1)
            return

        branch = "└── " if is_last else "├── "

        if node.is_leaf:
            node_value = repr(node.value)
        elif isinstance(node.value, (dict, list, tuple, set)):
            node_value = f"{type(node.value).__name__} with {len(node.value)} items"
        elif hasattr(node.value, "__dict__"):
            node_value = f"Object of type {type(node.value).__name__}"
        else:
            node_value = repr(node.value)

        print(f"{prefix}{branch}{node.path} = {node_value}")

        new_prefix = prefix + ("    " if is_last else "│   ")

        for i, child in enumerate(node.children):
            is_last_child = i == len(node.children) - 1
            self._print_tree(child, new_prefix, is_last_child, depth + 1)


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
