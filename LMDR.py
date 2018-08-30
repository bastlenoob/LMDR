import discord
import asyncio
import os
import datetime

bot = discord.Client()

heure = ''
spamLimit = datetime.timedelta(0,10,0)

async def testSpam():
	pass

@bot.event
async def on_message(message):
	global heure
	global spamLimit
	if heure == '':
		heure = message.timestamp
	elif message.timestamp != heure:
		# Récupération de la différence d'heure
		diff = message.timestamp - heure
		if diff <= spamLimit:
			print("Wesh c'est du spam ça !")
		else:
			heure = message.timestamp


# ========================================================
# Récupération du jeton dans le fichier "token.txt"
# ========================================================
empty = True
if os.path.isfile("token.txt"):
	fichier = open("token.txt", "r")
	token = fichier.read()
	if token != '' :
		empty = False
	fichier.close()

elif not os.path.isfile("token.txt") or empty == True:
	print("Récupération du jeton impossible.")
	exit()
bot.run(token)