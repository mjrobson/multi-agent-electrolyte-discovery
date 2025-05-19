import json
import operator
from typing import Annotated, Sequence
from typing_extensions import TypedDict

from langchain_core.messages import (
    BaseMessage,
    FunctionMessage,
    HumanMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools.render import format_tool_to_openai_function
from langgraph.prebuilt.tool_executor import ToolInvocation


# === Define Shared Agent State === #
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


# === Agent Creation === #
def create_agent(llm, tools, system_message: str):
    """Create an agent node that binds LLM and tools with a collaborative prompt."""
    functions = [format_tool_to_openai_function(t) for t in tools]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to make progress toward answering the question."
                    " If you cannot fully answer, that's OK—another assistant with different tools"
                    " will continue. If you or any assistant has the final answer or deliverable,"
                    " prefix your response with FINAL ANSWER so the team knows to stop."
                    " If no one can fully answer the question, do your best anyway. This is a challenging"
                    " topic that may require creating new ideas."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                ),
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
    return prompt | llm.bind_functions(functions)


# === Agent Node === #
def agent_node(state: AgentState, agent, name: str):
    """Run the agent with the current state and return its output as a message."""
    result = agent.invoke(state)

    # Ensure result is a message we can add to state
    if not isinstance(result, FunctionMessage):
        result = HumanMessage(**result.dict(exclude={"type", "name"}), name=name)

    return {
        "messages": [result],
        "sender": name,
    }


# === Tool Node === #
def tool_node(state: AgentState):
    """Call a tool based on the last agent message, and return the result."""
    messages = state["messages"]
    last_message = messages[-1]

    # Parse tool input from function call
    tool_input = json.loads(last_message.additional_kwargs["function_call"]["arguments"])
    if len(tool_input) == 1 and "__arg1" in tool_input:
        tool_input = next(iter(tool_input.values()))

    tool_name = last_message.additional_kwargs["function_call"]["name"]

    action = ToolInvocation(tool=tool_name, tool_input=tool_input)

    # Execute the tool
    response = tool_executor.invoke(action)

    # Return the result as a FunctionMessage
    return {
        "messages": [
            FunctionMessage(
                content=f"{tool_name} response: {str(response)}",
                name=action.tool,
            )
        ]
    }


# === Router === #
def router(state: AgentState):
    """Decide the next step: call a tool, end, or continue."""
    last_message = state["messages"][-1]

    if "function_call" in last_message.additional_kwargs:
        return "call_tool"
    if "FINAL ANSWER" in last_message.content:
        return "end"
    return "continue"
