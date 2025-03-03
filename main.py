# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def slack_conversations():
    # Replace with your token and channel ID
    TOKEN = "xoxb-your-token"
    CHANNEL_ID = "your-channel-id"

    # Fetch last 50 messages
    response = requests.get(
        "https://slack.com/api/conversations.history",
        headers={"Authorization": f"Bearer {TOKEN}"},
        params={"channel": CHANNEL_ID, "limit": 50}
    ).json()

    messages = response.get("messages", [])

    # Fetch threads for each message
    for message in messages:
        if "thread_ts" in message:
            thread_ts = message["thread_ts"]
            thread_response = requests.get(
                "https://slack.com/api/conversations.replies",
                headers={"Authorization": f"Bearer {TOKEN}"},
                params={"channel": CHANNEL_ID, "ts": thread_ts}
            ).json()
            print(f"Thread for message {thread_ts}: {thread_response.get('messages', [])}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm23')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
