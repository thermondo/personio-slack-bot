from pprint import pprint

import chat

mapping = chat.user_email_mapping()

for channel_id in chat.my_channels():
    pprint(channel_id)
    pprint(
        [
            mapping[user_id]
            for user_id in chat.channel_members(channel_id)
            if user_id in mapping
        ]
    )
