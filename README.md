# Person.io Slack Bot

A slack bot with person.io integration.

## Setting up the bot

Just click the button, duh!

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Thermondo/personio-slack-bot)

You must configure [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler) to run one of the commands below you want to use.

## Setting up Slack

https://api.slack.com/
-> 'Start Building'

### 1. Add Bot

In the section 'Add features and functionality' select Bots and fill the form

### 2. Permissions

In the section 'Add features and functionality' select Permissions

In the Scope add

* channels:read
* chat:write
* users:read
* users:read.email

### 3. Install your app to your workspace

Until this moment you have a bot configure but not installed in your workspace yet.
To do it and have access to Slack API credentials, click on _Install your app to your workspace_.

### 5. Set environment variables on the Heroku app

* `SLACK_BOT_TOKEN`: in the section _Install App_, copy it from _Bot User OAuth Access Token_.

Other environment variables that are optional:

* `SENTRY_DSN`: for Sentry integration purposes
* `PUBLIC_TIME_OFF_TYPES`: comma-separated list of time-off-type-names which should be public.

## Commands for the scheduler

### send daily time-off reminder

`python send_time_off_reminders.py`

For every channel this bot is invited, it will get the member-list.
Then with their email-addresses it will find time-offs of the channel-members for the current day and generates a message for these in this channel.

All time-off-types are treated private, so are not shown in the message. You can define exceptions in `PUBLIC_TIME_OFF_TYPES` that are then shown separately.
