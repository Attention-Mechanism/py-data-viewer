import os
from typing import Any, Optional
from .types import TreeNode, DataViewer


def file_output(data: Any, file_path: str, var_name: Optional[str] = None):
    """
    Outputs the exploration of a data structure to a file.

    Args:
        data (Any): The data structure to explore.
        file_path (str): The path to the output file.
        var_name (Optional[str], optional): Variable name for the root of the data structure. Defaults to None.
    """
    # Ensure the file has a .txt extension
    if not file_path.endswith(".txt"):
        file_path += ".txt"

    # Create a DataViewer instance
    explorer = DataViewer(data, colorize=False, var_name=var_name or "data")

    # Build the tree structure
    explorer.tree_root = TreeNode(explorer.var_name, explorer.data)
    explorer._build_tree(explorer.data, explorer.var_name, explorer.tree_root)

    # Write the tree to the file
    with open(file_path, "w", encoding="utf-8") as file:

        def write_tree(node: TreeNode, prefix: str = "", is_last: bool = True, depth: int = 0):
            if depth == 0:
                file.write(f"{node.path}\n")
                for i, child in enumerate(node.children):
                    is_last_child = i == len(node.children) - 1
                    write_tree(child, "", is_last_child, depth + 1)
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

            file.write(f"{prefix}{branch}{node.path} = {node_value}\n")

            new_prefix = prefix + ("    " if is_last else "│   ")

            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                write_tree(child, new_prefix, is_last_child, depth + 1)

        write_tree(explorer.tree_root)

    print(f"Data tree successfully written to {os.path.abspath(file_path)}")
