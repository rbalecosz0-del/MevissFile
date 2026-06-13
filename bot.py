import requests
import json
import time
import string
import secrets
import os


TOKEN = "13618647:3F3cWJq9rFLgbsUG0wTk7EgHkG7sXp-6BAv"

API = f"https://api.safew.bot/bot{TOKEN}"

DB = "data.json"



# =================
# DATABASE
# =================

def load():

    if not os.path.exists(DB):
        return {}

    try:
        return json.load(open(DB))

    except:
        return {}



def save(data):

    json.dump(
        data,
        open(DB,"w"),
        indent=2
    )



# =================
# CODE
# =================

def make_code():

    chars = string.ascii_lowercase + string.digits

    return (
        "mevissbot_"
        + secrets.choice(chars)
        + "v_"
        + secrets.choice(chars)
        + "p_"
        + secrets.choice(chars)
        + "d_"
        + "".join(
            secrets.choice(chars)
            for i in range(16)
        )
    )



# =================
# MESSAGE
# =================

def send(chat,text):

    r = requests.post(
        API+"/sendMessage",
        json={
            "chat_id":chat,
            "text":text
        }
    )

    print(r.text)



# =================
# SEND FILE
# =================

def send_file(chat,data):

    fid = data["file_id"]
    tipe = data["type"]


    if tipe == "photo":

        url = "/sendPhoto"
        key = "photo"


    elif tipe == "video":

        url = "/sendVideo"
        key = "video"


    else:

        url = "/sendDocument"
        key = "document"



    r = requests.post(
        API+url,
        json={
            "chat_id":chat,
            key:fid
        }
    )


    print("SEND FILE:")
    print(r.text)



# =================
# FILE DETECT
# =================

def check_file(msg):


    if "document" in msg:

        return {
            "type":"document",
            "file_id":msg["document"]["file_id"]
        }



    if "photo" in msg:

        return {
            "type":"photo",
            "file_id":msg["photo"][-1]["file_id"]
        }



    if "video" in msg:

        return {
            "type":"video",
            "file_id":msg["video"]["file_id"]
        }


    return None



# =================
# RUN
# =================

offset = 0


print("MEVISSBOT ONLINE")


while True:


    try:


        updates = requests.get(
            API+"/getUpdates",
            params={
                "offset":offset
            }
        ).json()



        for update in updates.get("result",[]):


            offset = update.get(
                "update_id",
                0
            ) + 1



            msg = (
                update.get("message")
                or update
            )



            chat = msg.get(
                "chat",
                {}
            ).get("id")



            if not chat:
                continue



            text = msg.get(
                "text",
                ""
            )



            if text == "/start":


                send(
                    chat,
"""🔥 MevissBOT AKTIF

📤 Kirim file

📥 Ambil file:
GET kode

Contoh:
GET mevissbot_8v_3p_0d_xxxxx"""
                )



            elif text.startswith("GET "):


                code = text.replace(
                    "GET ",
                    ""
                )


                db = load()



                if code in db:


                    send(
                        chat,
                        "⏳ Mengirim file..."
                    )


                    send_file(
                        chat,
                        db[code]
                    )


                else:


                    send(
                        chat,
                        "❌ Kode tidak ditemukan"
                    )



            else:


                file = check_file(msg)



                if file:


                    code = make_code()


                    db = load()


                    db[code] = file


                    save(db)



                    send(
                        chat,
f"""✅ File tersimpan

🔑 CODE:

{code}

📥 GET {code}

🤖 MevissBOT"""
                    )



    except Exception as e:

        print(
            "ERROR:",
            e
        )



    time.sleep(2)
