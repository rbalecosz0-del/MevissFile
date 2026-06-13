import requests
import json
import time
import random


TOKEN = "13618647:3F3cWJq9rFLgbsUG0wTk7EgHkG7sXp-6BAv"

API = f"https://api.safew.bot/bot{TOKEN}"

DB = "data.json"


# =================
# DATABASE
# =================

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


# =================
# SEND MESSAGE + BUTTON
# =================

def send(chat_id, text, button=True):

    url = API + "/sendMessage"


    data = {
        "chat_id": chat_id,
        "text": text
    }


    if button:

        data["reply_markup"] = {

            "keyboard":[

                [
                    {"text":"📤 Up File"},
                    {"text":"📥 Get File"}
                ]

            ],

            "resize_keyboard":True

        }


    requests.post(
        url,
        json=data
    )



# =================
# SEND FILE
# =================

def send_file(chat_id,file_id):

    requests.post(
        API+"/sendDocument",
        json={
            "chat_id":chat_id,
            "document":file_id
        }
    )



# =================
# MAIN
# =================

offset = 0

print("BOT ONLINE")



while True:

    try:

        updates = requests.get(
            API+"/getUpdates",
            params={
                "offset":offset
            }
        ).json()



        for update in updates.get("result",[]):

            offset = update["update_id"]+1


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



            # START

            if text == "/start":

                send(
chat,
"""🔥 Service ON✅

😋 Selamat datang di MevissFILE.

━━━━━━━━━━━━

📌 MENU

📤 Up File → upload file

📥 Get File → ambil file pakai CODE

━━━━━━━━━━━━

💀 NOTE

• CODE hilang tanggung jawab user
• Jangan spam 😉"""
                )




            # TOMBOL UP FILE

            elif text == "📤 Up File":

                send(
                    chat,
                    "📤 Silahkan kirim file kamu.",
                )




            # TOMBOL GET FILE

            elif text == "📥 Get File":

                send(
                    chat,
                    "📥 Kirim CODE file.\n\nContoh:\nGET 123456"
                )




            # GET CODE

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




            # UPLOAD FILE

            elif "document" in msg:


                file_id = msg["document"]["file_id"]


                code = str(
                    random.randint(
                        100000,
                        999999
                    )
                )


                db = load()


                db[code]=file_id


                save(db)



                send(
chat,
f"""📦 File berhasil disimpan 😉

🔑 CODE :
{code}

📥 Pakai:
GET {code}

🤖 MevissFILE"""
                )



    except Exception as e:

        print(e)



    time.sleep(2)
