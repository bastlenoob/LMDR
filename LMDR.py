import discord
import asyncio
import os
import datetime

# Initialisation du bot
bot = discord.Client()

# Initialisation des variables globales
heureMess = ''
heureMent = ''
messLimit = datetime.timedelta(0,20,0)
menLimit = datetime.timedelta(0,40,0)
listeMessages = []
listeMentions = []
listeAvertissements = []

# Déclaration de la fonction de test
async def testSpam(message, listeMessages, listeMentions):
	# Initialise le ban sur False, le bénéfice du doute
	ban = False
	# Récupère l'auteur
	author = message.author
	# Initialise le compteur à 0
	cpt = 0
	# Pour chaque message dans la liste des messages stockés
	for mess in listeMessages:
		# Si l'auteur du message est également l'auteur d'un autre message dans la liste
		if mess.author == author:
			# Incrémente le compteur de 1
			cpt+=1
	# Si l'auteur du message a envoyé 10 messages ou plus
	if cpt >= 11:
		# On procédera au banissement
		ban = True
	else:
		# Sinon on remet le compteur à 0
		cpt = 0
	# Pour chaque message dans la liste des messages contenant une ou plusieures mentions
	for mess in listeMentions:
		# Si l'auteur est également l'auteur d'un des messages
		if mess.author == author:
			# On incrémente le compteur de 1
			cpt+=1
	# Si l'auteur a écrit plus de un message
	if cpt >= 2:
		# On procède au bannissement
		ban = True
	# Si la sentence est tombée
	if ban == True:
		# On procède au bannissement
		# Encore en tests, pas de bannissement effectif pour l'instant
		await bot.send_message(message.channel, "Bip, Boup ! Bot LMDR Bonjour, Veuillez cesser de Spam.")
		await bot.send_message(message.channel, "Un avertissement pour : " + message.author.name + " Il n'y en aura pas de second.")
		# Cherche si l'auteur du message est dans la liste des avertissements
		for i in listeAvertissements:
			if i == message.author:
				present = True
		# Si il est présent on part sur un ban avant de le retirer de la liste
		if present == True:
			await bot.ban(message.author, 1)
			await bot.send_message(message.channel, "Donc là on part sur un kokoban des familles dans la gueule de : ", message.author.name)
			listeAvertissements.remove(message.author)
		else:
			listeAvertissements.append(message.author)

# Quand un message est posté
@bot.event
async def on_message(message):
	if not message.author.bot:
		# Récupération des variables globales
		global heureMess
		global heureMent
		global messLimit
		global menLimit
		global listeMessages
		global listeMentions
		global listeAvertissements

		# Si aucun timer de message n'est lancé
		if heureMess == '':
			# Démarre le premier timer et ajoute le premier message à la liste des messages
			heureMess = message.timestamp
			listeMessages.append(message)
		else:
			# Récupération de la différence d'heure entre ce message et celui qui a déclenché le timer
			diff = message.timestamp - heureMess
			# Si ça moins longtemps que la durée définie
			if diff <= messLimit:
				# On ajoute le message à la liste
				listeMessages.append(message)
			# Sinon
			else:
				# Déclenche un nouveau timer
				heureMess = message.timestamp
				# Supprime la liste des messages
				listeMessages.clear()
				print("J'oublie les messages")
				print(listeMessages)
				# Si un timer pour les mentions est en cours
				if heureMent != '':
					# Teste où en est le timer
					diffMent = message.timestamp - heureMent
					# Si le timer des mentions est fini
					if diffMent > menLimit:
						# Supprime la liste des mentions et prépare un nouveau timer
						listeMentions.clear()
						heureMent = ''
						print("J'oublie les mentions")
						print(listeMentions)

			# Si le message contient une mention
			if message.mentions:
				# Si aucun timer en cours
				if heureMent == '':
					# Initialise un timer et ajoute le message à la liste des mentions
					heureMent = message.timestamp
					listeMentions.append(message)
				# Sinon
				else:
					# Teste où en est le timer
					diffMent = message.timestamp - heureMent
					# Si le timer n'est pas terminé
					if diffMent <= menLimit:
						# Ajoute le message à la liste des mentions
						listeMentions.append(message)
					# Si le timer est terminé
					else:
						# En démarre un nouveau
						heureMent = message.timestamp
			# Appel la fonction testSpam en indiquand le message ainsi que les différentes listes
			# Pour tester si un ban est mérité ou non
			await testSpam(message, listeMessages, listeMentions)

			# Teste si l'utilisateur a envoyé un lien :
			if "www." in message.content or "http" in message.content or "discord.gg" in message.content:
				if message.channel.name != "youtube":
					# Teste la présence dans la liste des avertissements
					present = False
					
					for i in listeAvertissements:
						if i == message.author:
							present = True
					# Si il est présent, un avertissement a déjà eu lieu --> ban (Et suppression de la liste)
					if present == True:
						#await bot.ban(message.author, 1)
						await bot.send_message(message.channel, "Donc là on part sur un kokoban sur : " + message.author.name)
						listeAvertissements.remove(message.author)
					# Sinon ajout dans la liste des avertissements
					else:
						listeAvertissements.append(message.author)
						await bot.send_message(message.channel, "Un avertissement pour : " + message.author.name + " Il n'y en aura pas de second.")
					# Supprime le message
					await bot.delete_message(message)

			# Si une pièce jointe (genre photo) avec le message
			if message.attachments:
				# Teste la présence dans la liste des avertissements
				present = False
				for i in listeAvertissements:
					if i == message.author:
						present = True
				# Si dans la liste, ban et retrait de la liste
				if present == True:
					await bot.ban(message.author, 1)
					await bot.send_message(message.channel, "Donc là on part sur un kokoban sur : " + message.author.name)
					listeAvertissements.remove(message.author)
				# Sinon ajout dans la liste
				else:
					listeAvertissements.append(message.author)
					await bot.send_message(message.channel, "Un avertissement pour : " + message.author.name + " Il n'y en aura pas de second.")
				# Supprime le message
				await bot.delete_message(message)


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