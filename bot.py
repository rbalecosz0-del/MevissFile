import requests
import json
import time
import string
import secrets


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
# GENERATE CODE
# =================

def generate_code():

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
            for _ in range(16)
        )
    )



# =================
# SEND MESSAGE
# =================

def send(chat_id,text):

    requests.post(
        API+"/sendMessage",
        json={
            "chat_id":chat_id,
            "text":text
        }
    )



# =================
# SEND FILE
# =================

def send_file(chat_id,data):

    file_id = data["file_id"]
    tipe = data["type"]


    if tipe == "photo":

        requests.post(
            API+"/sendPhoto",
            json={
                "chat_id":chat_id,
                "photo":file_id
            }
        )


    elif tipe == "video":

        requests.post(
            API+"/sendVideo",
            json={
                "chat_id":chat_id,
                "video":file_id
            }
        )


    else:

        requests.post(
            API+"/sendDocument",
            json={
                "chat_id":chat_id,
                "document":file_id
            }
        )



# =================
# BOT LOOP
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



            # START

            if text == "/start":

                send(
                    chat,
"""🔥 MevissBOT AKTIF

📤 Kirim file untuk upload

📥 GET kode untuk ambil file

Contoh:
GET mevissbot_xv_xp_xd_xxxxx"""
                )



            # GET FILE

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
                        "❌ File tidak ditemukan"
                    )



            # FILE DOCUMENT

            elif "document" in msg:


                file_id = msg["document"]["file_id"]


                code = generate_code()


                db = load()


                db[code] = {

                    "type":"document",
                    "file_id":file_id

                }


                save(db)


                send(
                    chat,
f"""✅ File tersimpan

🔑 CODE:

{code}

📥 Ambil:
GET {code}

🤖 MevissBOT"""
                )



            # PHOTO

            elif "photo" in msg:


                file_id = msg["photo"][-1]["file_id"]

                code = generate_code()


                db = load()


                db[code]={

                    "type":"photo",
                    "file_id":file_id

                }


                save(db)


                send(
                    chat,
f"""✅ Foto tersimpan

🔑 CODE:
{code}

GET {code}"""
                )



            # VIDEO

            elif "video" in msg:


                file_id = msg["video"]["file_id"]

                code = generate_code()


                db = load()


                db[code]={

                    "type":"video",
                    "file_id":file_id

                }


                save(db)


                send(
                    chat,
f"""✅ Video tersimpan

🔑 CODE:
{code}

GET {code}"""
                )



    except Exception as e:

        print("ERROR:",e)



    time.sleep(2)
