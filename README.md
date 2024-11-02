# Hack Overflow Slack App

The [Hack Overflow](https://overflow.craigg.hackclub.app) Slack app allows users to ask and answer questions directly from the Hack Club Slack. It helps to bring Hack Overflow one step closer to achieving its goals of consolidating Hack Club's knowledge and making it easier to give and get help.

## Commands

The Hack Overflow Slack app provides three commands to users: `/overflow-apikey`, `/ask-question`, and `/answer-question`.

### `/overflow-apikey`

The `/overflow-apikey` command must be run before executing any other Hack Overflow commands. It sends a request to the Hack Overflow API to retrieve the user's API key. This key is then stored and used to run any future commands.

### `/ask-question`

The `/ask-question` command can be used to post a question to Hack Overflow on behalf of the user. This question is then sent to the [#overflow channel](https://hackclub.slack.com/archives/C07SS5ED09K) on Slack, along with its Question ID.

### `/answer-question`

The `/answer-question` command can be used to answer a question posted using `/ask-question`. Answers are sent in the thread of the question and are also posted to Hack Overflow. The first answer from each user is posted to Hack Overflow if a user submits multiple answers.

## Implementation Details

Every question posted using the Hack Overflow Slack app has two Question IDs. The ID sent to the Slack is the timestamp of the question message, which is stored as a key in the question database. The other ID is the ID created by Hack Overflow, which is stored as the value. This allows the `/answer-question` command to find the Hack Overflow question from the Slack message timestamp which is shown to the user.