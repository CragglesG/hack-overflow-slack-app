from slack_bolt import App
from requests import request
from dotenv import load_dotenv
import pickledb
import json
import os

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])

api_keys = pickledb.load("keys.db", auto_dump=True)

questions = pickledb.load("questions.db", auto_dump=True)

@app.command("/ask-question")
def ask_question(ack, body, logger, client):
	ack()
	with open("views/ask-modal.json") as f:
		client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("ask-modal")
def ask_modal(ack, body, logger, client):
	ack()
	print(body)
	title = body["view"]["state"]["values"][body["view"]["blocks"][0]["block_id"]]["question-title"]["value"]
	question = body["view"]["state"]["values"][body["view"]["blocks"][1]["block_id"]]["question-body"]["value"]
	if api_keys.get(body["user"]["id"]) == False:
		client.chat_postEphemeral(channel="C07SS5ED09K", user=body["user"]["id"], text="You need to generate your API key first. Run `/overflow-apikey` to generate it.")
	else:
		add_question = request("POST", "https://overflow.craigg.hackclub.app/answer/api/v1/question", headers={"Authorization": api_keys.get(body["user"]["id"])}, json={
			"content": question,
			"tags": [
				{
				"display_name": "from-slack",
				"original_text": "from-slack",
				"slug_name": "from-slack"
				}
			],
			"title": title
		})
		message1 = client.chat_postMessage(channel="C07SS5ED09K", blocks=[
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"*NEW QUESTION*\n*Title:* {title}\n\n{question}"
				}
			}
		])
		client.chat_postMessage(channel="C07SS5ED09K", thread_ts=message1["ts"], text=f"Question ID: {message1["ts"]}")
		questions.set(message1["ts"], add_question.json()["data"]["id"])

@app.command("/answer-question")
def answer_question(ack, body, logger, client):
	ack()
	with open("views/answer-modal.json") as f:
		client.views_open(trigger_id=body["trigger_id"], view=json.load(f))

@app.view_submission("answer-modal")
def answer_modal(ack, body, logger, client):
	ack()
	question_id = body["view"]["state"]["values"][body["view"]["blocks"][0]["block_id"]]["question-title"]["value"]
	answer = body["view"]["state"]["values"][body["view"]["blocks"][1]["block_id"]]["question-body"]["value"]
	profile = client.users_info(user=body["user"]["id"])["user"]["profile"]
	username = profile["display_name"]
	image = profile["image_original"]
	if api_keys.get(body["user"]["id"]) == False:
		client.chat_postEphemeral(channel="C07SS5ED09K", user=body["user"]["id"], text="You need to generate your API key first. Run `/overflow-apikey` to generate it.")
	elif questions.get(question_id) == False:
		client.chat_postEphemeral(channel="C07SS5ED09K", user=body["user"]["id"], text="Invalid question ID. Check that you typed in the question ID correctly. If you did, DM @Craig for assistance.")
	else:
		add_answer = request("POST", "https://overflow.craigg.hackclub.app/answer/api/v1/answer", headers={"Authorization": api_keys.get(body["user"]["id"])}, json={
			"content": answer,
			"question_id": questions.get(question_id)
		})
		client.chat_postMessage(channel="C07SS5ED09K", thread_ts=question_id, username=username, icon_url=image, blocks=[
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{answer}"
				}
			}
		], text=answer)

@app.command("/overflow-apikey")
def api_key(ack, body, logger, client):
	ack()
	if api_keys.get(body["user_id"]) == False:
		with open("views/apikey-modal.json") as f:
			client.views_open(trigger_id=body["trigger_id"], view=json.load(f))
	else:
		client.chat_postEphemeral(channel="C07SS5ED09K", user=body["user_id"], text=f"You already generated an API key! Your API key will automatically be used when you post questions or answers, but here it is anyway: `{api_keys.get(body['user_id'])}`")

@app.view_submission("apikey-modal")
def apikey_modal(ack, body, logger, client):
	ack()
	email = body["view"]["state"]["values"][body["view"]["blocks"][1]["block_id"]]["email"]["value"]
	password = body["view"]["state"]["values"][body["view"]["blocks"][2]["block_id"]]["password"]["value"]
	user_login = request("POST", "https://overflow.craigg.hackclub.app/answer/api/v1/user/login/email", json={"e_mail": email, "pass": password})
	api_keys.set(body["user"]["id"], user_login.json()["data"]["access_token"])
	client.chat_postEphemeral(channel="C07SS5ED09K", user=body["user"]["id"], text=f"Your API key has been generated!")

if __name__ == "__main__":
	app.start(port=int(os.environ.get("PORT", 3000)))