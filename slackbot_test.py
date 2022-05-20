from slack_bot import SlackBot

token = ""
message = "hello, <@U02PTPHGRCM>"
picture_as_message = "http://airbnb.io/img/projects/airflow3.png"
# slack_bot = SlackBot("@U02PTPHGRCM", token)
slack_bot = SlackBot("#robot-test", token)

#example
# slack_bot.send_picture_as_message(picture_as_message)
slack_bot.send_message(message)
# filepath = "test.txt"
# slack_bot.send_file(filepath)