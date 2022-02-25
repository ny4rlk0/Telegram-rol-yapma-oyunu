#!/usr/bin/python
#coding=utf-8
#https://github.com/ny4rlk0/Telegram-rol-yapma-oyunu/
import telepot,telepot.loop,telepot.namedtuple
import sqlite3,threading,os,time,pprint,random,validators,base64,json,subprocess
import configparser as c

xTOXEN="AX23xad21d922jd923u2"
db_exists=os.path.exists("database.db")
conn=sqlite3.connect("database.db", check_same_thread=False)
cur=conn.cursor()
if not db_exists:
    cur.execute("CREATE TABLE user (id INT, username CHAR(50), firstname VARCHAR(51),lastname CHAR(52), rol CHAR(50))")
    conn.commit()
    del cur
set_exists=os.path.exists("degerler.txt")
if not set_exists:
    cp = c.RawConfigParser()
    cp.add_section('veri')
    cp.set('veri', 'TOXEN', xTOXEN)
    setup = open('degerler.txt', 'w')
    cp.write(setup)
    setup.close()
nya = c.RawConfigParser()
nya.read('degerler.txt')
TOXEN = nya['veri'] ['TOXEN']

### Ayarlar
bot=telepot.Bot(TOXEN)

def handle(msg):
   try:
    pprint.pprint(msg)
    cur=conn.cursor()
    et="@"
    userid=msg["from"]["id"]
    chatid=msg["chat"]["id"]
    try:
        username=et+msg["from"]["username"]
    except:
        username=""
    try:
        firstname=msg["from"]["first_name"]
    except:
        firstname=""
    try:
        lastname=msg["from"]["last_name"]
    except:
        lastname=""
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

    if text.startswith("/rol ") or text.startswith("/Rol ") or text.startswith("/r "):
        cur.execute(f"SELECT id FROM user WHERE id={userid}")
        if len(cur.fetchall())==0:#user don't exist
            cur.execute(f"INSERT INTO user VALUES ('{userid}','{username}','{firstname}','{lastname}','??')")
            conn.commit()
        text=text.split(" ")
        hedef_rol=str(text[1])
        cur.execute(f"Update user set rol='{hedef_rol}' where id='{userid}'")
        conn.commit()
    
    if text=="/roller" or text=="/Roller" or text=="/göster":
        rolveri=""
        bos=" : "
        bbos=" "
        sonraki_satir="\n"
        cur.execute("SELECT id,username,firstname,lastname,rol from user")
        rlko=cur.fetchall()
        for nya in rlko:
            rolveri+=nya[1]+bbos+nya[2]+bbos+nya[3]+bos+nya[4]+sonraki_satir
        bot.sendMessage(chatid,f"{rolveri}")
        

    if text=="/reset" or text=="/Reset" or text=="/rr":
        cur.execute("DELETE FROM user")
        conn.commit()
        bot.sendMessage(chatid,"Oyun sıfırlandı.")
    
    if text=="/yardim" or text=="/help":
        bot.sendMessage(chatid,"Komutlar /rol ROLADI, /roller, /reset\nHer oyun başında oyuna katılmak istiyenler /oyna yazar.\nPeşine rollerinizi /rol ISTENENROL olarak yazarsınız.\nEn son /roller komutuyla kimin ne oldugu gorulur.\nOyunu /reset ile sıfırlar.\nA NYARLKO Creation.")
   except:
       pass
if __name__ == "__main__":
    telepot.loop.MessageLoop(bot,handle).run_forever()
