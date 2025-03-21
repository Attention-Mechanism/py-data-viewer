```python
from any_agent_framework import AsyncAI
from data_viewer import vprint

async def assistant_run_stream() -> None:
    response = await AsyncAI()
    vprint(response, "response")

if __name__ == "__main__":
    import asyncio

    asyncio.run(assistant_run_stream())
```

beautiful (to me) output
```shell
response
├── response.chat_message = Object of type ToolCallSummaryMessage
│   ├── response.chat_message.source = 'Assistant'
│   ├── response.chat_message.models_usage = None
│   ├── response.chat_message.metadata = dict with 0 items
│   ├── response.chat_message.content = 'AutoGen is a programming framework for building multi-agent applications.'
│   └── response.chat_message.type = 'ToolCallSummaryMessage'
└── response.inner_messages = list with 2 items
    ├── response.inner_messages[0] = Object of type ToolCallRequestEvent
    │   ├── response.inner_messages[0].source = 'Assistant'
    │   ├── response.inner_messages[0].models_usage = Object of type RequestUsage
    │   │   ├── response.inner_messages[0].models_usage.prompt_tokens = 22
    │   │   └── response.inner_messages[0].models_usage.completion_tokens = 6
    │   ├── response.inner_messages[0].metadata = dict with 0 items
    │   ├── response.inner_messages[0].content = list with 1 items
    │   │   └── response.inner_messages[0].content[0] = Object of type FunctionCall
    │   │       ├── response.inner_messages[0].content[0].id = ''
    │   │       ├── response.inner_messages[0].content[0].arguments = '{"query":"AutoGen"}'
    │   │       └── response.inner_messages[0].content[0].name = 'web_search'
    │   └── response.inner_messages[0].type = 'ToolCallRequestEvent'
    └── response.inner_messages[1] = Object of type ToolCallExecutionEvent
        ├── response.inner_messages[1].source = 'Assistant'
        ├── response.inner_messages[1].models_usage = None
        ├── response.inner_messages[1].metadata = dict with 0 items
        ├── response.inner_messages[1].content = list with 1 items
        │   └── response.inner_messages[1].content[0] = Object of type FunctionExecutionResult
        │       ├── response.inner_messages[1].content[0].content = 'AutoGen is a programming framework for building multi-agent applications.'
        │       ├── response.inner_messages[1].content[0].name = 'web_search'
        │       ├── response.inner_messages[1].content[0].call_id = ''
        │       └── response.inner_messages[1].content[0].is_error = False
        └── response.inner_messages[1].type = 'ToolCallExecutionEvent'
```