import os
import pymongo
from pymongo import MongoClient
import time
import datetime
import telepot
from telepot.loop import MessageLoop
import socket

TOKEN = "Token" #Yout Token from Bot Telegram

def getMongoData():
	client = MongoClient('mongodb://127.0.0.1:27017')
	db = client["online_news"]
	collection01 = db["db_1"]
	collection02 = db["db_2"]

	all_msg = []
	msg0 = "HASHING IMAGE INSERT MONGO REPORT \n"
	all_msg.append(msg0)

	pubdate05 = collection05.find().sort("pubdate", pymongo.DESCENDING).limit(1)
	for date_hash05 in pubdate05:
		msgPubdate05 = "Last pubdate month 05:\n {}\n".format(date_hash05['pubdate'])
		all_msg.append(msgPubdate05)

	pubdate04 = collection04.find().sort("pubdate", pymongo.DESCENDING).limit(1)
	for date_hash04 in pubdate04:
		msgPubdate04 = "Last pubdate month 04:\n {}\n".format(date_hash04['pubdate'])
		all_msg.append(msgPubdate04)
	
	message = "\n".join(all_msg)
	client.close()
	return message

def CekServer():
	with open("/directory/bot_hash_mongo/server_list.txt", "r") as f:
		server_list = f.read().splitlines()
		f.close()

	up_server = []
	down_server = []
	for server in server_list:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
		    s.connect((server, 22))
		    up_server.append(server)
		except:
		    down_server.append(server)
		s.close()
	message = "Server Up:\n{}\n\nServer Down:\n{}".format("\n".join(up_server), "\n".join(down_server))
	return message

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	try:
		if content_type == 'text':
			text = msg['text']
			print("{} -> {}".format(chat_id, text))
			# if "/cvs" in text:
			if "cek" in text:
				message = getMongoData()
				bot.sendMessage(chat_id, message, parse_mode='Markdown')
			elif "server" in text:
				message = CekServer()
				bot.sendMessage(chat_id, message, parse_mode='Markdown')
			else:
				bot.sendMessage(chat_id, "Command Not Found")
			# else:
			# 	bot.sendMessage(chat_id, "Command Not Found. use '/cvs help'")
	except Exception as e:
		print(e)

if __name__=="__main__":
	bot = telepot.Bot(TOKEN)
	MessageLoop(bot, handle).run_as_thread()
	print('Listening ...')

	while 1:
		time.sleep(10)