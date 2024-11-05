import requests
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

user_id = # enter userid of the user your targetting.
timeperrequest = 5 # edit inverval where it checks (2 requests)
Webhook = "" # DO NOT SHARE, enter webnhook url here

cookie = "" # DO NOT SHARE, enter FULL roblox cookie here NOT JUST ROBLOXSECURITY

checkwearing = 0
outfitchanged = 0
getuser = 0
first = 0
oldwear = []

embed = DiscordEmbed()

headers = {
    'cookie': cookie
}

while True:
    data = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing", headers=headers)
    headshot = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png&isCircular=false")
    if getuser == 0:
        user = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        user = user.json()
        name = user.get("name", [])
    status1 = data.status_code
    print(f"Status Code: {status1}")
    data = data.json()
    headshot = headshot.json()
    headshoturl = headshot.get("data", {})
    headshoturl2 = headshoturl[0].get("imageUrl")
    if headshoturl2:
        embed.set_image(url=headshoturl2)
    else:
        embed.set_image(url='https://static.wikia.nocookie.net/roblox/images/6/66/Content_Deleted.png/revision/latest/scale-to-width-down/250?cb=20230428000418')

    active = data.get("assetIds", [])
    length = len(active)
    print(f"amount of assets wearing: {length}")
    if first == 0 and active != []:
        oldwear = active
        webhook = DiscordWebhook(url=Webhook, content=f"Targetting **{name}** :dart:\nTheir current avatar consists of {active}")
        webhook.add_embed(embed)
        response = webhook.execute()
        first = 1
    elif first == 0 and active == []:
        webhook = DiscordWebhook(url=Webhook, content=f"Targetting **{name}**:dart:\nTheir current avatar is **Blank!**")
        oldwear = active
        webhook.add_embed(embed)
        response = webhook.execute()
        first = 1
    if checkwearing == 0:
        checkwearing = 1
    elif checkwearing == 1:
        if oldwear != active:
            print(f"{name} has changed their outfit: ids = {active}")
            added = set(active) - set(oldwear)
            lossed = set(oldwear) - set(active)
            if active == []:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit! \nbut they set it so a **Blank Avatar** \n**Removed**: {lossed}")
                webhook.add_embed(embed)
                response = webhook.execute()
                oldwear = active
                time.sleep(timeperrequest)
            elif added and lossed:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Added**: {added} \n**Removed**: {lossed}")
                webhook.add_embed(embed)
                response = webhook.execute()
                print("none is null")
                oldwear = active
                time.sleep(timeperrequest)
            elif lossed:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Nothing Added** \n**Removed**: {lossed}")
                webhook.add_embed(embed)
                response = webhook.execute()
                print("added is null")
                oldwear = active
                time.sleep(timeperrequest)
            elif added:
                webhook = DiscordWebhook(url=Webhook, content=f"**{name}** has changed their outfit!: \n**Wearing**: = {active} \n**Added**: {added} \n**Nothing Removed**")
                webhook.add_embed(embed)
                response = webhook.execute()
                print("loss is null")
                oldwear = active
                time.sleep(timeperrequest)
            checkwearing = 0
        else:
            print("outfit is the same")
            time.sleep(timeperrequest)
