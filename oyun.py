#!/usr/bin/python
#coding=utf-8
#FUCK OFF SQL INJECTION
import telepot,telepot.loop,telepot.namedtuple
import sqlite3,threading,os,time,pprint,random,validators,base64,json,subprocess
db_exists=os.path.exists("database.db")
conn=sqlite3.connect("database.db", check_same_thread=False)
cur=conn.cursor()
if not db_exists:
    cur.execute("CREATE TABLE user (id INT, firstname VARCHAR(256), rol CHAR(50))")
    conn.commit()
    del cur
### Ayarlar
bot=telepot.Bot("Buraya BOT TOXENI GIR")
ADMINS=[BURAYA ADMIN USER ID VIRGULLE AYIRARAK GIR 000,1111 gibi]
##Buraları kendine göre değiştir.

def handle(msg):
    global userid
    pprint.pprint(msg)
    cur=conn.cursor()
    userid=msg["from"]["id"]
    chatid=msg["chat"]["id"]
    data=""
    if "data" in msg.keys():
        data=msg["data"]
    text=""
    if "document" in msg.keys():
        text="FileID:"+msg["document"]["file_id"]
    elif "photo" in msg.keys():
        text="FileID:"+msg["photo"][0]["file_id"]
    else:
        text=msg["text"]

    if text.startswith("/oyna"):
        cur.execute(f"SELECT id FROM user WHERE id={userid}")
        if len(cur.fetchall())==0:#user don't exist
            cur.execute(f"INSERT INTO user VALUES ({userid},'{msg['from']['first_name']}','??')")
            conn.commit()
            bot.sendMessage(chatid,"Bu oyunda sizde yeralacaksınız.")
        else:
            bot.sendMessage(chatid,"Bu oyunda sizde yeralacaksınız.")

    if text.startswith("/rol ") or text.startswith("/Rol "):
        text=text.split(" ")
        hedef_rol=str(text[1])
        cur.execute(f"Update user set rol='{hedef_rol}' where id='{userid}'")
        conn.commit()
        bot.sendMessage(chatid,"Rolünüz belirlendi.")
    
    if text=="/roller" or text=="/Roller":
        bot.sendMessage(chatid,"Roller:")
        cur.execute("SELECT firstname,rol from user")
        rlko=cur.fetchall()
        for nya in rlko:
            bot.sendMessage(chatid,f"Ad: {nya[0]}\nRol: {nya[1]}\n")

    if text=="/reset" or text=="/Reset" and userid in ADMINS:
        cur.execute("DELETE FROM user")
        conn.commit()
        bot.sendMessage(chatid,"Oyun sıfırlandı.")
    
    if text=="/yardim" or text=="/help" and userid in ADMINS:
        bot.sendMessage(chatid,"Komutlar /oyna, /rol ROLADI, /roller, /reset")
        bot.sendMessage(chatid,"Her oyun başında oyuna katılmak istiyenler /oyna yazar.")
        bot.sendMessage(chatid,"Peşine rollerinizi /rol ISTENENROL olarak yazarsınız.")
        bot.sendMessage(chatid,"En son /roller komutuyla kimin ne oldugu gorulur.")
        bot.sendMessage(chatid,"Admin oyunu /reset ile sıfırlar.")

if __name__ == "__main__":
    telepot.loop.MessageLoop(bot,handle).run_forever()