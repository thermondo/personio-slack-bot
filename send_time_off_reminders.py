from datetime import date
from itertools import groupby

import chat
import personio

slack_user_mapping = chat.user_email_mapping()

time_off_for_today = personio.approved_time_off_for(date_=date.today())

for channel_id in chat.my_channels():
    emails = {
        slack_user_mapping[user_id]
        for user_id in chat.channel_members(channel_id)
        if user_id in slack_user_mapping
    }

    time_off_for_this_channel = sorted(
        [to for to in time_off_for_today if to.email in emails],
        key=lambda t: (t.type_, t.email),
    )

    msg = "*_Who is off today?_* \n"

    for type_, time_off_list in groupby(time_off_for_this_channel, lambda x: x.type_):
        msg += f"*{type_}*\n"

        for to in time_off_list:
            msg += f"- {to.first_name} {to.last_name}"

            if to.end_date and to.end_date.date() != date.today():
                msg += (
                    " (until "
                    f"<!date^{int(to.end_date.timestamp())}^{{date_short_pretty}}|"
                    f"{to.end_date.date().isoformat()}>"
                    ")"
                )

            msg += "\n"

        msg += "\n"

    chat.post_message(channel_id, msg)
