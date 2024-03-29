import slack
from slackclient import SlackClient
import pathlib
import json
import time

current_dir = pathlib.Path(__file__).parent
with open(f"{current_dir}/config.txt", encoding='utf-8') as json_file:
    config = json.load(json_file)
slack_token = config['slack_api_token']
sc = SlackClient(slack_token)
web_client = slack.WebClient(token=config['slack_api_token'])


def get_message_event(event):
    # start here
    # print(event)
    web_client.chat_postMessage(
        channel=event['channel'],
        text=event['text'],
    )


if sc.rtm_connect(with_team_state=False, auto_reconnect=True):
    while sc.server.connected is True:
        events = sc.rtm_read()
        # print(events)
        for event in events:
            if 'type'in event and event['type'] == "message" and 'user' in event:
                get_message_event(event)
        time.sleep(0.5)
else:
    print("Connection Failed")

