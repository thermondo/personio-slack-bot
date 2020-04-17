from datetime import date
from itertools import groupby

import chat
import config
import personio


def _timeoff_slack_message(time_off_list):
    msg = ""
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

    return msg


def send_time_off_reminders():
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
            key=lambda t: t.email,
        )

        msg = "*_Who is off today?_* \n"

        msg += _timeoff_slack_message(
            [
                to
                for to in time_off_for_this_channel
                if to.type_ not in config.PUBLIC_TIME_OFF_TYPES
            ]
        )

        for public_type in config.PUBLIC_TIME_OFF_TYPES:
            time_off = [
                to for to in time_off_for_this_channel if to.type_ == public_type
            ]
            if time_off:
                msg += f"\n*{public_type}*\n"
                msg += _timeoff_slack_message(time_off)

        chat.post_message(channel_id, msg)


if __name__ == "__main__":
    send_time_off_reminders()
