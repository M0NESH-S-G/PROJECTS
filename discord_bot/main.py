import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

sad_words = ["sad", "unhappy", "depressed", "miserable", "depressing"]

starter_encouragements = ["Cheer up","You are a great person!", "Chin up"]

if "responding" not in db:
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update(encouraging_message):
  if "encouragments" in db:
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  

@client.event
async def on_ready():
    print('We logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith("$hello"):
      await message.channel.send('HELLO!')
      
    if msg.startswith("$inspire"):
      qoute = get_quote()
      await message.channel.send(qoute)

    if db["responding"]:
      options = starter_encouragements
      if "encouragements" in db:
        options += db["encouragements"]
        
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith("$new"):
      encouraging_message = msg.split("$new ",1)[1]
      update(encouraging_message)
      await message.channel.send("New Encouraging Message Added. ")
      
    if msg.startswith("$del"):
      encouragements = []
      if "encouragements" in db:
        index = int(msg.split("$del",1)[1])
        delete(index)
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$list"):
      encouragements = []
      if "encouragements" in db:
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("$responding"):
      value = msg.split("responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is ON. ")
      else:
        db["responding"] = False
        await message.channel.send("Responding is OFF. ")
keep_alive()
client.run(os.getenv('TOKEN'))

