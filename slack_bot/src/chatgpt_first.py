from slack_sdk import WebClient

async def show_modal(shortcut, client:WebClient, callback_id):
    # 組み込みのクライアントを使って views_open メソッドを呼び出す
    await client.views_open(
        trigger_id=shortcut["trigger_id"],
        # モーダルで表示するシンプルなビューのペイロード
        view={
            "type": "modal",
            "callback_id": callback_id,
            "title": {
                "type": "plain_text",
                "text":"ChatGPT"
            },
            "submit": {
                "type": "plain_text",
                "text": "送信"
            },
            "close": {
                "type": "plain_text",
                "text":"キャンセル"
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "label": {
                        "type": "plain_text",
                        "text": "タイトル"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_input"
                    }
                },
                {
                    "type": "input",
                    "block_id": "question_block",
                    "label": {
                        "type": "plain_text",
                        "text": "質問"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "question_input",
                        "multiline": True
                    }
                }
            ]
        }
    )
