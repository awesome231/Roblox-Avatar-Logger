import requests
import time
from discord_webhook import DiscordWebhook

user_id = #set target's userid here
timeperrequest = 5 # edit time per request
Webhook = "" # DO NOT SHARE, enter your webhook

cookie = "" # DO NOT SHARE, your FULL roblox cookie, not just ROBLOSECURITY!!

checkwearing = 0
outfitchanged = 0
getuser = 0
first = 0
oldwear = []



headers = {
    'cookie': cookie
}

while True:
    data = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing", headers=headers)
    if getuser == 0:
        user = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        user = user.json()
        name = user.get("name", [])
    status1 = data.status_code
    print(f"Status Code: {status1}")
    data = data.json()

    active = data.get("assetIds", [])
    length = len(active)
    print(f"amount of assets wearing: {length}")
    if first == 0 and active != []:
        webhook = DiscordWebhook(url=Webhook, content=f"Targetting **{name}** :dart:\nTheir current avatar consists of {active}")
        response = webhook.execute()
        first = 1
    elif first == 0 and active == []:
        webhook = DiscordWebhook(url=Webhook, content=f"Targetting **{name}**:dart:\nTheir current avatar is **Blank!**")
        response = webhook.execute()
        first = 1
    if checkwearing == 0:
        oldwear = active
        print("defaulting to new outfit")
        checkwearing = 1
        time.sleep(timeperrequest)
    elif checkwearing == 1:
        if oldwear != active:
            print(f"{name} has changed their outfit: ids = {active}")
            added = set(active) - set(oldwear)
            lossed = set(oldwear) - set(active)
            if active == []:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit! \nbut they set it so a **Blank Avatar** \n**Removed**: {lossed}")
                response = webhook.execute()
            elif added and lossed:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Added**: {added} \n**Removed**: {lossed}")
                response = webhook.execute()
                print("none is null")
            elif lossed:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Nothing Added** \n**Removed**: {lossed}")
                response = webhook.execute()
                print("added is null")
            elif added:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Added**: {added} \n**Nothing Removed**")
                response = webhook.execute()
                print("loss is null")
            checkwearing = 0
            time.sleep(timeperrequest)
        else:
            print("outfit is the same")
            time.sleep(timeperrequest)
