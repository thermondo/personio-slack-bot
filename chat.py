from slack import WebClient

import config

slack_client = WebClient(config.SLACK_BOT_TOKEN)


def my_channels():
    return [
        channel["id"]
        for channel in slack_client.channels_list(exclude_archived=1)["channels"]
        if channel["is_member"] is True
    ]


def channel_members(channel_id):
    return slack_client.channels_info(channel=channel_id)["channel"]["members"]


def user_email_mapping():
    return {
        user["id"]: user["profile"]["email"]
        for user in slack_client.users_list()["members"]
        if (
            user["deleted"] is False
            and user["is_bot"] is False
            and "email" in user["profile"]
        )
    }


def post_message(channel_id, text):
    slack_client.chat_postMessage(
        channel=channel_id, text=text,
    )
