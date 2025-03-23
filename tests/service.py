# Mock classes to represent the structure of the response object
class ToolCallSummaryMessage:
    def __init__(self, source, models_usage, metadata, content, type_):
        self.source = source
        self.models_usage = models_usage
        self.metadata = metadata
        self.content = content
        self.type = type_


class RequestUsage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class FunctionCall:
    def __init__(self, id_, arguments, name):
        self.id = id_
        self.arguments = arguments
        self.name = name


class ToolCallRequestEvent:
    def __init__(self, source, models_usage, metadata, content, type_):
        self.source = source
        self.models_usage = models_usage
        self.metadata = metadata
        self.content = content
        self.type = type_


class FunctionExecutionResult:
    def __init__(self, content, name, call_id, is_error):
        self.content = content
        self.name = name
        self.call_id = call_id
        self.is_error = is_error


class ToolCallExecutionEvent:
    def __init__(self, source, models_usage, metadata, content, type_):
        self.source = source
        self.models_usage = models_usage
        self.metadata = metadata
        self.content = content
        self.type = type_


# Function to generate the mock response object
def generate_mock_response():
    response = {}

    # Creating the chat_message object
    response["chat_message"] = ToolCallSummaryMessage(
        source="Assistant",
        models_usage=None,
        metadata={},
        content=("Acetaminophen can mask a fever but may reduce the risk of adverse events such as" " seizures."),
        type_="ToolCallSummaryMessage",
    )

    # Creating the inner_messages list
    response["inner_messages"] = []

    # Adding ToolCallRequestEvent
    tool_call_request_event = ToolCallRequestEvent(
        source="Assistant",
        models_usage=RequestUsage(prompt_tokens=22, completion_tokens=6),
        metadata={},
        content=[FunctionCall(id_="", arguments='{"query":"AutoGen"}', name="web_search")],
        type_="ToolCallRequestEvent",
    )
    response["inner_messages"].append(tool_call_request_event)

    # Adding ToolCallExecutionEvent
    tool_call_execution_event = ToolCallExecutionEvent(
        source="Assistant",
        models_usage=None,
        metadata={},
        content=[
            FunctionExecutionResult(
                content=(
                    "Acetaminophen can mask a fever but may reduce the risk of adverse events such" " as seizures."
                ),
                name="web_search",
                call_id="",
                is_error=False,
            )
        ],
        type_="ToolCallExecutionEvent",
    )
    response["inner_messages"].append(tool_call_execution_event)

    return response
