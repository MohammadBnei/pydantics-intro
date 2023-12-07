from pydantic import BaseModel, field_validator
import instructor
from openai import OpenAI
from collections.abc import Callable
from openai_function_calling.tool_helpers import ToolHelpers
import json

client = instructor.patch(OpenAI())


def sum(a, b):
    """Sum description adds a + b"""
    return a + b + 2


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    tools=ToolHelpers.infer_from_function_refs([sum]),
    messages=[{"role": "user", "content": "Sum 2 + 3"}],
)

print(response.choices)

response_message = response.choices[0].message

if response_message.tool_calls is not None:
    avalaibe_functions: dict[str, Callable] = {
        "sum": sum
    }
    
    tool_call = response_message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
    
    function_args = json.loads(arguments)

    function_ref = avalaibe_functions[function_name]
    result = function_ref(**function_args)
    print(result)

class UserDetail(BaseModel):
    name: str
    age: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v.upper() != v:
            raise ValueError("name must be in uppercase")
        return v

    def __str__(self) -> str:
        return f"name: {self.name}, age: {self.age}"


client = instructor.patch(OpenAI())

user = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=UserDetail,
    max_retries=3,
    messages=[{"role": "user", "content": "I am jason and i am 26 years old"}],
)

print(user)
