from gpt_tmp import api as gpt_api

async def send(question_text):
    
    # TODO:中間API層に送信
    anser_text = await gpt_api.getChatGpt(question_text)

    return anser_text
