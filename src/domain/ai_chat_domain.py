import discord
import dto
import os
import error
from network import open_ai_network


async def send_thread_to_ai(messages: list[discord.Message], bot_user: discord.ClientUser) -> str:
    chat_messages = [dto.ChatMessage(dto.Role.ASSISTANT if m.author == bot_user else dto.Role.USER, m.content)
                     for m in messages]

    chat_request = dto.ChatRequest(os.environ.get('CHAT_SYSTEM_INSTRUCTION'), chat_messages)

    try:
        response = await open_ai_network.send_chat_completion_request(chat_request)

        return response.choices[0].message.content
    except error.TokenQuotaReachedError:
        return "Sorry! I've reached my limit for this month. " \
               "Please ask the administrator to check their OpenAI billing details."
    except error.UnexpectedNetworkError:
        return "Sorry! An unknown error occurred. Please contact the administrator for details."
