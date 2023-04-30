import os

import openai

# APIキーの設定
openai.api_key = os.environ["OPENAI_API_KEY"]

async def getChatGpt(que):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": que},
        ],
    )

    return response.choices[0]["message"]["content"].strip()
