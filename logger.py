import requests
import time
from discord_webhook import DiscordWebhook

user_id =  # set target's user id here
timeperrequest = 4 # change each time it sends a request (2 requests are sent during the duration)
Webhook = # enter your discord webhook DO NOT SHARE

cookie = "" # enter your FULL ROBLOX COOKIE, NOT JUST ROBLOSECURITY. DO. NOT. SHARE. THIS.

checkwearing = 0
outfitchanged = 0
first = 0
oldwear = []

headers = {
    'cookie': cookie
}

while True:
    data = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing", headers=headers)
    user = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
    status1 = data.status_code
    status2 = user.status_code
    print(f"Status Code: Currently wearing: {status1} UserID: {status2}")
    data = data.json()
    user = user.json()

    active = data.get("assetIds", [])
    name = user.get("name", [])
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
        time.sleep(3)
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
            time.sleep(3)
        else:
            print("outfit is the same")
            time.sleep(3)
