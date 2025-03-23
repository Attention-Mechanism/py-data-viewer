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
