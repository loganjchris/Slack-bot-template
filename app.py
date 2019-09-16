import os
import logging
import ssl as ssl_lib
import json
import certifi
import slack
from message_reader import reader
from save_sheets import google_lookup


#When a message is sent
@slack.RTMClient.run_on(event="message")
def message(**payload):

    """When a message is sent in the slack server, first separate all the data.
    Discard all the messages that will crash. This include anything without
    messages, or unwanted subtypes. Can call save sheets if keyword is triggered.
    Otherwise, pass message to message_reader.py to get a response. Also logs
    responses to add to the spreadsheet or troubleshoot issues
    """

    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    subtype = data.get("subtype")

    #If you want the bot to only respond in a single channel, set the channel ID here
    channel_lock = ("")


    #Only want to respond in the specified channel
    if channel_id not in channel_lock:
        return

    #Don't respond to bots or message changes
    if subtype:
        return

    #Fixes crash when text is empty
    if text in (" ", ""):
        return

    #If the Source data is changed, we want to update the local version, so call the script that updates it
    if text.lower() == "update me":
        google_lookup()
        return

    if "Pssst!" in text:
        #Funny story, when sending a link more than one time in an hour, slack will respond with a message about unfurling a link
        #more than once in an hour. I can't remeber exactly what it says but it begins with "Pssst!". This was the best way I could find to
        #not respond when receiving this message
        return


    #Send response
    else:
        #I want to know what people ask the bot because it's being used in a dedicated channel for it,
        #if you use this bot in a channel with a lot of none related traffic, I would disable these two text files
        f = open("responselist.txt", "a")
        f.write(user_id + ": " + text.replace(u"\u2018", "'").replace(u"\u2019", "'") + "\n")
        f.close()

        #Write messages to file for analysis later
        with open('join_message.txt', 'a', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write('\n')


        #If there isn't a keyword in the database, don't respond
        bot_response = (reader(text.lower))
        if not bot_response:
            return

        else:
            #Send the designated response in the channel the mesasge came from
            web_client.chat_postMessage(
                channel = channel_id,
                text = bot_response,
                as_user = True
            )

if __name__ == "__main__":
    #Logging will output information into the console
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    #Uses ssl for security
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    #Assumes that your bot token is saved as an environment variable
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
