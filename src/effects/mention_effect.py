import discord
from domain import ai_chat_domain
import config


async def on_bot_mention(message: discord.Message, bot_user: discord.ClientUser):

    if bot_user in message.mentions and not config.active_threads.__contains__(message.id):
        thread = await message.create_thread(name='Chatting', auto_archive_duration=60)
        config.active_threads.append(thread.id)

        async with thread.typing():
            bot_response = await ai_chat_domain.send_thread_to_ai([message], bot_user)
            await thread.send(content=bot_response)
