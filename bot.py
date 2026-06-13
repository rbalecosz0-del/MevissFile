import requests
import json
import time
import random


# =====================
# TOKEN BOT
# =====================

TOKEN = "13618647:3F3cWJq9rFLgbsUG0wTk7EgHkG7sXp-6BAv"

API = f"https://api.safew.bot/bot{TOKEN}"

DB = "data.json"



# =====================
# DATABASE
# =====================

def load():
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



# =====================
# ENDPOINT SEND MESSAGE
# =====================

def send(chat_id, text):

    url = API + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(
        url,
        json=data
    )



# =====================
# SEND FILE
# =====================

def send_file(chat_id, file_id):

    url = API + "/sendDocument"

    data = {
        "chat_id": chat_id,
        "document": file_id
    }

    requests.post(
        url,
        json=data
    )



# =====================
# GET UPDATE
# =====================

offset = 0


print("BOT ONLINE")


while True:

    try:

        url = API + "/getUpdates"

        res = requests.get(
            url,
            params={
                "offset":offset
            }
        ).json()



        for update in res.get("result",[]):

            offset = update["update_id"] + 1


            msg = update.get(
                "message",
                {}
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



            # =================
            # START
            # =================

            if text == "/start":


                send(
chat,
"""🔥 BOT ONLINE

😉 Selamat datang di MevissFILE.

━━━━━━━━━━━━

📌 MENU

📤 Up File → upload file

📥 Get File → ambil file pakai CODE

━━━━━━━━━━━━

💀 NOTE

• CODE Meviss
• Jangan spam 😉"""
                )




            # =================
            # GET FILE
            # =================

            elif text.startswith("GET "):


                code = text.replace(
                    "GET ",
                    ""
                )


                db = load()



                if code in db:


                    send_file(
                        chat,
                        db[code]
                    )


                else:

                    send(
                        chat,
                        "❌ CODE tidak ditemukan"
                    )




            # =================
            # UPLOAD FILE
            # =================

            elif "document" in msg:


                file_id = msg["document"]["file_id"]


                code = str(
                    random.randint(
                        100000,
                        999999
                    )
                )


                db = load()


                db[code] = file_id


                save(db)



                send(
chat,
f"""📦 Total File : 1

💾 File berhasil disimpan 😉

🔑 CODE :
{code}

🤖 Bot FileMeviss"""
                )



    except Exception as e:

        print(e)



    time.sleep(2)
