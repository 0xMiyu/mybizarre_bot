
import os
import time  
import telebot  
from telebot import types 
from jikanpy import Jikan
import random

jikan = Jikan()

API_KEY = os.environ["API_KEY"]
bot = telebot.TeleBot(API_KEY, parse_mode="Markdown")

############ MARKUPS #################


markupSTART = types.ReplyKeyboardMarkup(row_width=3)
btn1 = types.KeyboardButton('Search')
btn2 = types.KeyboardButton('Top Rated')
btn3 = types.KeyboardButton('Current Season')
btn4 = types.KeyboardButton('Upcoming')
btn5 = types.KeyboardButton('Music Search')
markupSTART.add(btn1, btn2, btn3, btn4, btn5)
 

markupTOP = types.ReplyKeyboardMarkup(row_width=2)
butt1 = types.KeyboardButton('Top Anime')
butt2 = types.KeyboardButton('Top Movies')
butt3 = types.KeyboardButton('Top Manga')
butt4 = types.KeyboardButton('Top Novels')
butt5 = types.KeyboardButton('/restart')
markupTOP.add(butt1, butt2, butt3, butt4, butt5)

############## ERROR FUNCTION #################

def sendError(m, cid, e):
  print("Exception: ",str(e))
  bot.send_message(cid,'Error Sadge - From Input:\n%s' %m.text, reply_markup=types.ReplyKeyboardMarkup().add(types.KeyboardButton("/restart")))

############### SEARCH FUNCTION ################

def searchResult(m, cid, type, query):
  try:
    result = jikan.search(type, query, page=1)
    searchMarkup = types.ReplyKeyboardMarkup()
    msg = '*Search Results*\n\n'
    for a in range(5):
      msg += '%d: %s\n' % (a + 1, result['results'][a]['title'])
      searchMarkup.add(types.KeyboardButton('Title: %s\n%sID %s' % (result['results'][a]['title'],type,result['results'][a]['mal_id'])))
    searchMarkup.add(types.KeyboardButton("/restart"))
    bot.send_message(cid, msg, reply_markup=searchMarkup)
  except Exception as e:
    sendError(m, cid, e)

def animeID(m, cid, id):
  
  # print(result)
  try:
    result = jikan.anime(id)
    title = '[Title: %s](%s)\n' % (result["title_english"],result["url"]) if result["title_english"] else '[Title: %s](%s)\n' % (result["title"],result["url"])
    score = 'Score: %s/10\n' % result["score"] if result["score"] else 'Score N.A.\n'
    rank = 'Rank #%d\n' % result["rank"] if result['rank'] else 'Rank N.A.\n' 
    status = 'Status: %s\n' % result["status"] if result['status'] else 'Status N.A.\n' 
    episodes = 'Episode(s): %s\n' % result["episodes"] if result['episodes'] else 'Episodes N.A.\n' 
    premiered = 'Date: %s' % result["aired"]["string"] if result['aired']['string'] else 'Date N.A.\n' 

    msg = title + score + rank + status + episodes + premiered
    relatedMarkup = types.ReplyKeyboardMarkup()
    # add prequels
    if "Prequel" in result["related"].keys():
      for prequel in result["related"]["Prequel"]:
        relatedMarkup.add(types.KeyboardButton('Prequel: %s\nanimeID %s' % (prequel["name"], prequel["mal_id"])))
    # add sequels
    if "Sequel" in result["related"].keys():
      for sequel in result["related"]["Sequel"]:
        relatedMarkup.add(types.KeyboardButton('Sequel: %s\nanimeID %s' % (sequel["name"], sequel["mal_id"])))
        
    relatedMarkup.add(types.KeyboardButton("/restart"))
    bot.send_photo(cid,result["image_url"],caption=msg, reply_markup=relatedMarkup)
  except Exception as e:
      sendError(m, cid, e)
 
def mangaID(m, cid, id):
  
  # print(result)
  try:
    result = jikan.manga(id)
    title = '[Title: %s](%s)\n' % (result["title_english"],result["url"]) if result["title_english"] else '[Title: %s](%s)\n' % (result["title"],result["url"])
    score = 'Score: %s/10\n' % result["score"] if result["score"] else 'Score N.A.\n'
    rank = 'Rank #%d\n' % result["rank"] if result['rank'] else 'Rank N.A.\n' 
    status = 'Status: %s\n' % result["status"] if result['status'] else 'Status N.A.\n' 
    # episodes = 'Episode(s): %s\n' % result["episodes"] if result['episodes'] else 'Episodes N.A.\n' 
    published = 'Date: %s' % result["published"]["string"] if result['published']['string'] else 'Date N.A.\n' 

    # msg = title + score + rank + status + episodes + date
    msg = title + score + rank + status + published #observing DylanChua
    relatedMarkup = types.ReplyKeyboardMarkup()
    # add prequels
    if "Prequel" in result["related"].keys():
      for prequel in result["related"]["Prequel"]:
        relatedMarkup.add(types.KeyboardButton('Prequel: %s\nmangaID %s' % (prequel["name"], prequel["mal_id"])))
    # add sequels
    if "Sequel" in result["related"].keys():
      for sequel in result["related"]["Sequel"]:
        relatedMarkup.add(types.KeyboardButton('Sequel: %s\nmangaID %s' % (sequel["name"], sequel["mal_id"])))
        
    relatedMarkup.add(types.KeyboardButton("/restart"))
    bot.send_photo(cid,result["image_url"],caption=msg, reply_markup=relatedMarkup)
  except Exception as e:
      sendError(m, cid, e)

############### MUSIC SEARCH FUNCTION ###############

def songsearchResult(m, cid, type, query):
  try:
    result = jikan.search(type, query, page=1)
    searchMarkup = types.ReplyKeyboardMarkup()
    msg = '*Search Results*\n\n'
    for a in range(5):
      msg += '%d: %s\n' % (a + 1, result['results'][a]['title'])
      searchMarkup.add(types.KeyboardButton('Title: %s\nsonganimeID %s' % (result['results'][a]['title'],result['results'][a]['mal_id'])))
    searchMarkup.add(types.KeyboardButton("/restart"))
    bot.send_message(cid, msg, reply_markup=searchMarkup)
  except Exception as e:
      sendError(m, cid, e)

def songanimeID(m, cid, id):
  try:
    result = jikan.anime(id)
    title = '[Title: %s](%s)\n' % (result["title_english"],result["url"]) if result["title_english"] else '[Title: %s](%s)\n' % (result["title"],result["url"])
    opening = "Opening(s):\n" + ''.join([op + '\n' for op in result["opening_themes"]])
    ending = "Ending(s):\n" + ''.join([ed + '\n' for ed in result["ending_themes"]])
    msg = title + opening + ending

    relatedMarkup = types.ReplyKeyboardMarkup()
    # add prequels
    if "Prequel" in result["related"].keys():
      for prequel in result["related"]["Prequel"]:
        relatedMarkup.add(types.KeyboardButton('Prequel: %s\nsonganimeID %s' % (prequel["name"], prequel["mal_id"])))
    # add sequels
    if "Sequel" in result["related"].keys():
      for sequel in result["related"]["Sequel"]:
        relatedMarkup.add(types.KeyboardButton('Sequel: %s\nsonganimeID %s' % (sequel["name"], sequel["mal_id"])))
    
    relatedMarkup.add(types.KeyboardButton("/restart"))

    bot.send_photo(cid,result["image_url"],caption=msg, reply_markup=relatedMarkup)
  except Exception as e:
      sendError(m, cid, e)


############ TOP RATED FUNCTIONS #################

def topResult(m,cid,type,subtype):
  try:
    result = jikan.top(type,0,subtype)
    msg = 'Top %s\n\n' % subtype.title()
    searchMarkup = types.ReplyKeyboardMarkup()
    if type != "anime":
      for a in range(5):
        msg += '%d: %s\n' % (a + 1, result['top'][a]['title'])
        searchMarkup.add(types.KeyboardButton('Title: %s\nmangaID %s' % (result['top'][a]['title'],result['top'][a]['mal_id'])))
    else:
      for a in range(5):
        msg += '%d: %s\n' % (a + 1, result['top'][a]['title'])
        searchMarkup.add(types.KeyboardButton('Title: %s\nanimeID %s' % (result['top'][a]['title'],result['top'][a]['mal_id'])))
    searchMarkup.add(types.KeyboardButton("/restart"))
    bot.send_message(cid, msg, reply_markup=searchMarkup)
  except Exception as e:
      sendError(m, cid, e)

############ CURRENT SEASON FUNCTION ##################

def currentSeason(m,cid):
  try:
    result = jikan.season()
    searchMarkup = types.ReplyKeyboardMarkup()
    msg = 'Top Current Season Anime\n\n'
    for a in range(5):
      msg += '%d: %s\n' % (a + 1, result['anime'][a]['title'])
      searchMarkup.add(types.KeyboardButton('Title: %s\nanimeID %s' % (result['anime'][a]['title'],result['anime'][a]['mal_id'])))
    searchMarkup.add(types.KeyboardButton("/restart"))
    bot.send_message(cid, msg, reply_markup=searchMarkup)
  except Exception as e:
      sendError(m, cid, e)

############ UPCOMING SEASON FUNCTION ##################

def upcoming(m,cid):
  try:
    result = jikan.season_later()
    searchMarkup = types.ReplyKeyboardMarkup()
    msg = 'Top Upcoming Anime\n\n'
    for a in range(5):
      msg += '%d: %s\n' % (a + 1, result['anime'][a]['title'])
      searchMarkup.add(types.KeyboardButton('Title: %s\nanimeID %s' % (result['anime'][a]['title'],result['anime'][a]['mal_id'])))
    searchMarkup.add(types.KeyboardButton("/restart"))
    bot.send_message(cid, msg, reply_markup=searchMarkup)
  except Exception as e:
    sendError(m, cid, e)

############### START MESSAGE HANDLER ################
@bot.message_handler(commands=['start', 'restart'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "whats up my dude", reply_markup=markupSTART)

############### SEARCH BY NAME MESSAGE HANDLER ################
@bot.message_handler(func=lambda message: len(message.text) == 6 and message.text.lower() == 'search')
def command_search(m):
    cid = m.chat.id
    bot.send_message(cid, "Please search in this format:\n\n'search \[_anime/manga_] \[_anime/manga name_]'", reply_markup=markupSTART)

@bot.message_handler(func=lambda message: len(message.text) > 16 and message.text[:13].lower() == 'search anime ')
def command_search(m):
    cid = m.chat.id
    searchResult(m, cid, "anime", m.text[13:])

@bot.message_handler(func=lambda message: len(message.text) > 16 and message.text[:13].lower() == 'search manga ')
def command_search(m):
    cid = m.chat.id
    searchResult(m, cid, "manga", m.text[13:])

def splitAnimeID(m):
  if chr(10) in m.text:
    m.text = m.text.split(chr(10))[1]
  return len(m.text) > 8 and m.text[:8].lower() == 'animeid '

@bot.message_handler(func=splitAnimeID)
def command_search(m):
    cid = m.chat.id
    animeID(m, cid, m.text[8:])

def splitMangaID(m):
  if chr(10) in m.text:
    m.text = m.text.split(chr(10))[1]
  return len(m.text) > 8 and m.text[:8].lower() == 'mangaid '

@bot.message_handler(func=splitMangaID)
def command_search(m):
    cid = m.chat.id
    mangaID(m, cid, m.text[8:])

############### MUSIC SEARCH MESSAGE HANDLER ################
@bot.message_handler(func=lambda message: len(message.text) == 12 and message.text.lower() == 'music search')
def command_search(m):
    cid = m.chat.id
    bot.send_message(cid, "To find the ED or OP of your anime,\nPlease search in this format:\n\n'music search \[_anime name_]'", reply_markup=markupSTART)

@bot.message_handler(func=lambda message: len(message.text) > 16 and message.text[:13].lower() == 'music search ')
def command_search(m):
    cid = m.chat.id
    songsearchResult(m, cid, "anime", m.text[13:])

def splitsongAnimeID(m):
  if chr(10) in m.text:
    m.text = m.text.split(chr(10))[1]
  return len(m.text) > 12 and m.text[:12].lower() == 'songanimeid '

@bot.message_handler(func=splitsongAnimeID)
def command_search(m):
    cid = m.chat.id
    songanimeID(m, cid, m.text[12:])

############### TOP RATED MESSAGE HANDLER ################   
@bot.message_handler(func=lambda message: message.text.lower() == 'top rated')
def command_top(m):
    cid = m.chat.id
    bot.send_message(cid, "Which Category?", reply_markup = markupTOP)

@bot.message_handler(func=lambda message: message.text.lower() == 'top anime')
def command_topAnime(m):
    cid = m.chat.id
    topResult(m,cid,"anime","TV")

@bot.message_handler(func=lambda message: message.text.lower() == 'top movies')
def command_topMovies(m):
    cid = m.chat.id
    topResult(m,cid,"anime","movie")

@bot.message_handler(func=lambda message: message.text.lower() == 'top manga')
def command_topManga(m):
    cid = m.chat.id
    topResult(m,cid,"manga","manga")

@bot.message_handler(func=lambda message: message.text.lower() == 'top novels')
def command_topNovels(m):
    cid = m.chat.id
    topResult(m,cid,"manga","novels")


############### CURRENT SEASON MESSAGE HANDLER ################
@bot.message_handler(func=lambda message: message.text.lower() == 'current season')
def command_current(m):
    cid = m.chat.id
    currentSeason(m,cid)

############### UPCOMING SEASON MESSAGE HANDLER ################
@bot.message_handler(func=lambda message: message.text.lower() == 'upcoming')
def command_upcoming(m):
    cid = m.chat.id
    upcoming(m,cid)

############### RANDOM MESSAGE HANDLER ################
@bot.message_handler(func=lambda message: message.text.lower() == 'cock rating')
def command_upcoming(m):
    cid = m.chat.id
    bot.send_message(cid, "%s/10" % random.randint(1, 10), reply_markup = types.ReplyKeyboardMarkup().add(types.KeyboardButton("/restart")))

@bot.message_handler(func=lambda message: message.text.lower() == 'fumo')
def command_upcoming(m):
    cid = m.chat.id
    bot.send_message(cid, "ᗜˬᗜ", reply_markup = types.ReplyKeyboardMarkup().add(types.KeyboardButton("/restart")))
    ############## POLLING #################

# bot.infinity_polling(interval=0, timeout=20)  <-- no idea what the diff is
bot.polling(none_stop=True)
while True: 
    time.sleep(300)