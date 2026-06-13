import requests
import json
import time
import string
import secrets
import os


TOKEN = os.getenv("TOKEN")

API = f"https://api.safew.bot/bot{TOKEN}"

DB = "data.json"



# =====================
# DATABASE
# =====================

def load():

    try:
        with open(DB,"r") as f:
            return json.load(f)

    except:
        return {}



def save(data):

    with open(DB,"w") as f:
        json.dump(
            data,
            f,
            indent=2
        )



# =====================
# CODE GENERATOR
# =====================

def make_code():

    chars = string.ascii_lowercase + string.digits

    return (
        "meviss_"
        + "".join(
            secrets.choice(chars)
            for i in range(24)
        )
    )



# =====================
# SEND MESSAGE
# =====================

def send(chat,text):

    requests.post(
        API+"/sendMessage",
        json={
            "chat_id":chat,
            "text":text
        },
        timeout=20
    )



# =====================
# SEND FILE
# =====================

def send_file(chat,data):

    if data["type"] == "document":

        requests.post(
            API+"/sendDocument",
            json={
                "chat_id":chat,
                "document":data["file_id"]
            }
        )


    elif data["type"] == "photo":

        requests.post(
            API+"/sendPhoto",
            json={
                "chat_id":chat,
                "photo":data["file_id"]
            }
        )


    elif data["type"] == "video":

        requests.post(
            API+"/sendVideo",
            json={
                "chat_id":chat,
                "video":data["file_id"]
            }
        )



# =====================
# DETECT FILE
# =====================

def detect_file(msg):


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



# =====================
# BOT LOOP
# =====================


offset = 0


print(
    "🔥 MEVISSBOT ONLINE",
    flush=True
)



while True:


    try:


        result = requests.get(
            API+"/getUpdates",
            params={
                "offset":offset,
                "timeout":30
            },
            timeout=40
        ).json()



        for update in result.get(
            "result",
            []
        ):


            offset = (
                update["update_id"]
                + 1
            )



            msg = update.get(
                "message",
                {}
            )


            chat = msg.get(
                "chat",
                {}
            ).get(
                "id"
            )


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
                    """
🔥 MevissBOT AKTIF

📤 Kirim file apa saja

Bot akan memberikan kode

📥 Ambil file:

GET kode
"""
                )



            # GET FILE

            elif text.startswith(
                "GET "
            ):


                code = text.replace(
                    "GET ",
                    ""
                ).strip()



                db = load()



                if code in db:


                    send_file(
                        chat,
                        db[code]
                    )


                else:


                    send(
                        chat,
                        "❌ Kode tidak ditemukan"
                    )



            # UPLOAD FILE

            else:


                file = detect_file(
                    msg
                )



                if file:


                    code = make_code()



                    db = load()


                    db[code] = file


                    save(db)



                    send(
                        chat,
                        f"""
✅ File berhasil disimpan

🔑 CODE:

{code}

📥 GET {code}

🤖 MevissBOT
"""
                    )




    except Exception as e:


        print(
            "ERROR:",
            e,
            flush=True
        )



    time.sleep(2)
