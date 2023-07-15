from enum import StrEnum
import os
from requests import auth


class BearerAPIKeyAuth(auth.AuthBase):
    token: str

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


class AccessTokenResponse:
    access_token: str
    expires_in: int
    token_type: str


class Role(StrEnum):
    SYSTEM = "system",
    USER = "user",
    ASSISTANT = "assistant",


class ChatMessage:
    role: Role
    content: str

    def __init__(self, role: Role, content: str):
        self.role = role
        self.content = content

    @staticmethod
    def from_json_dict(json_dict):
        return ChatMessage(
            json_dict['role'],
            json_dict['content'])


class ChatChoice:
    index: int
    message: ChatMessage
    finish_reason: str

    def __init__(self, index: int, message: ChatMessage, finish_reason: str):
        self.index = index
        self.message = message
        self.finish_reason = finish_reason

    @staticmethod
    def from_json_dict(json_dict):
        return ChatChoice(
            json_dict['index'],
            ChatMessage.from_json_dict(json_dict['message']),
            json_dict['finish_reason'])


class ChatUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __init__(self, prompt_tokens: int, completion_tokens: int, total_tokens: int):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens

    @staticmethod
    def from_json_dict(json_dict):
        return ChatUsage(
            json_dict['prompt_tokens'],
            json_dict['completion_tokens'],
            json_dict['total_tokens'])


class ChatRequest:
    model: str
    messages: list[ChatMessage]

    def __init__(self, system_instruction: str, existing_messages: list[ChatMessage]):
        self.model = os.environ.get('OPENAI_MODEL')

        messages = [ChatMessage(Role.SYSTEM, system_instruction)]
        messages.extend(existing_messages)
        self.messages = messages


class ChatResponse:
    id: str
    object: str
    created: int
    choices: list[ChatChoice]
    usage: ChatUsage

    def __init__(self, id: str, object: str, created: int, choices: list[ChatChoice], usage: ChatUsage):
        self.id = id
        self.object = object
        self.created = created
        self.choices = choices
        self.usage = usage

    @staticmethod
    def from_json_dict(json_dict):
        return ChatResponse(
            json_dict['id'],
            json_dict['object'],
            json_dict['created'],
            [ChatChoice.from_json_dict(c) for c in json_dict['choices']],
            ChatUsage.from_json_dict(json_dict['usage']))
