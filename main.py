from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import openai

from config import api_id, api_hash, openai_key
openai.api_key = openai_key





client = TelegramClient('anon', api_id, api_hash)

# Следите за новыми сообщениями в канале
@client.on(events.NewMessage(chats=('testcomi')))
async def new_message_handler(event):
    # Получите текст нового сообщения
    message_text = event.message.message

    # Используйте OpenAI для генерации комментария
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": message_text}],
        max_tokens=600
    )

    comment = response.choices[0].message['content'].strip()

    # Отправьте сгенерированный комментарий
    #await client.send_message('testcomi', comment)

    # Получите историю сообщений
    name = 'testcomi'
    posts = await client(GetHistoryRequest(
        peer=name,
        limit=1,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    if posts.messages:
        # Взять первое сообщение из истории
        post = posts.messages[0]

        # Отправить комментарий "w" в качестве ответа на сообщение
        await client.send_message(entity=name, message=comment, comment_to=post)

with client:
    client.run_until_disconnected()
