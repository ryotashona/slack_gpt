import os
from slack_sdk import WebClient

async def post_title(body, client:WebClient):
    # 投稿者
    user_id = body['user']['id']

    # 入力された質問タイトルを取得
    title = body['view']['state']['values']['title_block']['title_input']['value']

    # 質問タイトル投稿
    post_response = await client.chat_postMessage(
        channel=os.environ["CHANNEL_ID"],
        text=f"<@{user_id}>\n{title}"
        )
    return post_response

async def post_question(body, client:WebClient, thread_ts):

    # 入力された質問内容を取得
    question_text = body['view']['state']['values']['question_block']['question_input']['value']

    # botへのメンション用idを取得
    bot_info = await client.auth_test()
    chatgpt_bot_user_id = bot_info["user_id"]

    # 初回質問内容投稿
    await client.chat_postMessage(
        channel=os.environ["CHANNEL_ID"],
        text=f"<@{chatgpt_bot_user_id}>\n{question_text}",
        thread_ts=thread_ts
    )
    return question_text

