import os
import asyncio
from slack_sdk import WebClient
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

import chatgpt_first
import chatgpt_start
import chatgpt_request

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
bot_info = client.auth_test()

@app.shortcut("chatgpt_first")
async def handle_chatgpt_first(ack, shortcut, client):
    # ショートカットのリクエストを確認
    await ack()

    # 初回質問用モーダルを表示.
    await chatgpt_first.show_modal(shortcut, client, "chatgpt_start")

@app.view("chatgpt_start")
async def handle_chatgpt_start(ack, body, logger, client):   
    # フォームの送信を確認
    await ack()

    # 初回質問のタイトルを投稿.
    post_response = await chatgpt_start.post_title(body, client)

    # 初回質問をスレッドに投稿.
    thread_ts=post_response["ts"]
    question_text = await chatgpt_start.post_question(body, client, thread_ts)

    # TODO: API実行
    anser_text = await chatgpt_request.send(question_text)

    # 初回質問の回答をスレッドに
    await client.chat_postMessage(
        channel=os.environ["CHANNEL_ID"],
        text=f"{anser_text}",
        thread_ts=thread_ts
    )

@app.event("app_mention")
async def handle_app_mentions(body, logger):
    # メンションを受けたメッセージのts（タイムスタンプ）を取得
    thread_ts = body['event']['ts']

    # 質問用に投稿からメンションを削除
    post_text = body['event']['text']
    chatgpt_bot_user_id = bot_info["user_id"]
    question_text = post_text.replace(f"<@{chatgpt_bot_user_id}>", "")

    # TODO: API実行
    anser_text = await chatgpt_request.send(question_text)

    # 質問の回答をスレッドに
    await client.chat_postMessage(
        channel=os.environ["CHANNEL_ID"],
        text=f"{anser_text}",
        thread_ts=thread_ts
    )

async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
