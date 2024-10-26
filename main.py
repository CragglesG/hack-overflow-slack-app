from slack_bolt import App
from requests import request
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])

@app.command("/ask-question")
def ask_question(ack, body, logger, client):
    ack()
    with open("views/ask-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("ask-modal")
def start_hack_submission(ack, body, logger, client):
    ack()
    title = body["view"]["state"]["values"][body["view"]["blocks"][1]["block_id"]]["question-title"]["value"]
    question = body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["question-body"]["value"]
    client.chat_postMessage(channel="C07SS5ED09K", blocks=f"""[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*NEW QUESTION*\n*Title:* {title}\n\n{question}"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Question ID: {body['message']['ts']}",
					"emoji": true
				}
			]
		}
	]""")
	# TODO: API request to Hack Overflow goes here

@app.command("/answer-question")
def ask_question(ack, body, logger, client):
    ack()
    with open("views/answer-modal.json") as f:
        client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("answer-modal")
def start_hack_submission(ack, body, logger, client):
    ack()
    question_id = body["view"]["state"]["values"][body["view"]["blocks"][1]["block_id"]]["question-title"]["value"]
    answer = body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["question-body"]["value"]
	username = body["user"]["username"]
	image = client.users_info(user=body["user"]["id"])["user"]["image_512"]
    client.chat_postMessage(channel="C07SS5ED09K", thread_ts=question_id, username=username, image=image, blocks=f"""[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "{answer}"
			}
		}
	]""")
	# TODO: API request to Hack Overflow goes here
