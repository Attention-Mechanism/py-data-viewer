# Py-Data-Viewer

`py-data-viewer` is a lightweight Python library that makes exploring and navigating complex data structures in the terminal effortless. It provides a clear, tree-based visualization of nested dictionaries, lists, objects, and more, making debugging and data analysis more efficient. No more getting lost in complex nested structures or struggling to understand what's inside your data or how to access them! 

> _Trees for complex data structures, Trees for simple data structures, Trees for everything!!_

### No more confusion with complex data structures or asking "what's inside this dictionary!?"

```python
from py_data_viewer import vprint

async def some_async_fn():
    response = await some_api_call()
    vprint(response) # 👈 pass in full response or part of it! It can handle Iterables[of_any_T]!!
```
<img src="img/screen-2.webp" width=80% height=80%>

### No more looking for properties in a long list of dictionaries or objects while in the terminal!
```python
vprint(data, "result")
```

<img src="img/screen-1.webp" width=80% height=80%>


## Features

- **Tree View**: Visualize data structures in the terminal as a tree for better clarity.
- **Colorized Output**: Easily distinguish different parts of the data structure.
- **Supports Multiple Data Types**: Works with dictionaries, lists, objects, namedtuples, and mixed structures.
- **API Response Exploration**: Simplifies debugging and understanding of API responses, especially for complex outputs.
- **Programmatic Usage**: Integrate directly into your Python scripts with the `vprint` function.


## Installation

To install the package, use pip:

```bash
pip install py-data-viewer -U
```

Then, import:
```python
from py_data_viewer import vprint
```

## Usage

### Programmatic Usage with `vprint`

The `vprint` function is the easiest way to explore data structures in your Python scripts. It provides a tree-like visualization of your data, making it ideal for debugging API responses, especially from frameworks!

#### Example: Exploring an API Response

```python
from py_data_viewer import vprint

# Simulated API response
response = {
    "chat_message": {
        "source": "Assistant",
        "content": "This is a response from an LLM.",
        "metadata": {},
    },
    "inner_messages": [
        {
            "type": "ToolCallRequestEvent",
            "content": [{"name": "search", "arguments": '{"query":"example"}'}],
        },
        {
            "type": "ToolCallExecutionEvent",
            "content": [{"name": "search", "content": "Search result here."}],
        },
    ],
}

vprint(response, var_name="messages", colorize=False)
```

Output showing you exactly how to access the data you want:
```
messages
├── messages.chat_message = dict with 3 items
│   ├── messages.chat_message.source = 'Assistant'
│   ├── messages.chat_message.content = 'This is a response from an LLM.'
│   └── messages.chat_message.metadata = dict with 0 items
└── messages.inner_messages = list with 2 items
    ├── messages.inner_messages[0] = dict with 2 items
    │   ├── messages.inner_messages[0].type = 'ToolCallRequestEvent'
    │   └── messages.inner_messages[0].content = list with 1 items
    │       └── messages.inner_messages[0].content[0] = dict with 2 items
    │           ├── messages.inner_messages[0].content[0].name = 'search'
    │           └── messages.inner_messages[0].content[0].arguments = '{"query":"example"}'
    └── messages.inner_messages[1] = dict with 2 items
        ├── messages.inner_messages[1].type = 'ToolCallExecutionEvent'
        └── messages.inner_messages[1].content = list with 1 items
            └── messages.inner_messages[1].content[0] = dict with 2 items
                ├── messages.inner_messages[1].content[0].name = 'search'
                └── messages.inner_messages[1].content[0].content = 'Search result here.'
```

#### Example: Exploring a Complex Data Structure

```python
from py_data_viewer import vprint

data = {
    "user": {"id": 1, "name": "Alice"},
    "actions": [
        {"type": "login", "timestamp": "2023-01-01T12:00:00Z"},
        {"type": "purchase", "details": {"item": "book", "price": 12.99}},
    ],
}

vprint(data, var_name="data")
```


## Advanced Options

The `vprint` function supports several options to customize the output:

- `var_name`: Specify the variable name to display in the output.
- `colorize`: Enable or disable colorized output (default: `True`).

Example:
```python
vprint(data, var_name="custom_data_name", colorize=False)
```


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Links

- **Homepage**: [GitHub Repository](https://github.com/Attention-Mechanism/py-data-viewer)
- **Issues**: [Report Issues](https://github.com/Attention-Mechanism/py-data-viewer)
