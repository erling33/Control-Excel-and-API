from slack import WebClient
from slack.errors import SlackApiError


class SlackBot:
    payload = {
        "channel": "",
        "blocks": [

        ],
    }

    def __init__(self, channel, token):
        self.channel = channel
        self.token = token

    # set the channel
    def __decide_channel(self):
        self.payload["channel"] = self.channel

    # use the input message to change the payload content. this method will remove previous
    # message to prevent duplicate.
    def decide_message(self, message):
        m = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    message
                )
            }
        }
        for item in self.payload["blocks"]:
            self.payload["blocks"].remove(item)
        self.payload["blocks"].append(m)

    # use input url of picture to change the payload content.
    # this method will remove previous message to prevent duplicate.
    def decide_picture_as_message(self, pic_url):
        for item in self.payload["blocks"]:
            self.payload["blocks"].remove(item)
        accessory = dict(type="image", image_url=pic_url, alt_text="image")
        self.payload["blocks"].append(accessory)

    # craft and return the entire message payload as a dictionary.
    def __get_message_payload(self):
        self.__decide_channel()
        return self.payload

    def send_message(self, decide_message):
        slack_web_client = WebClient(self.token)
        self.decide_message(decide_message)
        message = self.__get_message_payload()
        slack_web_client.chat_postMessage(**message)

    def send_picture_as_message(self, decide_picture_as_message):
        slack_web_client = WebClient(self.token)
        self.decide_picture_as_message(decide_picture_as_message)
        message = self.__get_message_payload()
        slack_web_client.chat_postMessage(**message)

    def send_file(self, file_location):
        slack_web_client = WebClient(self.token)
        try:
            response = slack_web_client.files_upload(
                channels=self.channel,
                file=file_location
            )
            assert response["file"]  # the uploaded file
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")