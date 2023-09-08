import telebot
import os
import ejson
import time
import random
import math
import speech_recognition as sr
import soundfile as sf
#os.chdir("/home/cyborgkiller")
users = ejson.Json("users.json")
bot = telebot.TeleBot("5710456111:AAFMD74M2AdZOxv1pKBmVDQL_ZFyuekwl00")
pings = users["pingoff"]["users"]
PI = math.pi
version = "v0.9.1-vt.ck_jenya"
def sin(i):
    return math.sin(math.radians(i))
def cos(i):
    return math.cos(math.radians(i))
def tg(i):
    return math.tag(math.radians(i))
def asin(i):
    return math.degrees(math.asin(i))
def acos(i):
    return math.degrees(math.acos(i))
def atg(i):
    return math.degrees(math.atag(i))
def ceil(i):
    return math.ceil(i)
def sqrt(i):
    return math.sqrt(i)
@bot.message_handler(commands=['ping_off'])
def ping_off(message):
        pings.append(message.from_user.username)
        users.update()
        bot.reply_to(message, "Пінги: вимкнені. Ви той кого не можна називати!")
@bot.message_handler(commands=['ping_on'])
def ping_on(message):
        if message.from_user.username in users['admins'] or True:
            pings.remove(message.from_user.username)
            users.update()
            bot.reply_to(message, "Пінги: увімкнені. Ви втратили свою владу!")
        else:
            bot.reply_to(message, "Ви не адміністратор!")
@bot.message_handler(commands=["about"])
def profile(message):
    bot.reply_to(message, f"Бот створено @vladtopordev\nДопомогли: @NickTel, @parameterlovervexik\nДізнатися про оновлення: https://t.me/cyborg_killerbot\nВерсія: {version}")

@bot.message_handler(func=lambda m: True)
def handler(message):
    users["ids"][message.from_user.username] = message.from_user.id
    try:
        users["stats"]["msg"][message.from_user.username] += 1
    except:
        users["stats"]["msg"][message.from_user.username] = 1
    users.update()
    if message.text.startswith("/unmute "):
        if message.from_user.username in users['admins'] or "vladtopordev" in message.text:

            args = message.text.split(" ")
            bot.restrict_chat_member(message.chat.id, int(users["ids"][args[1]]), until_date=time.time()+35)
            bot.reply_to(message, "Ви добра людина!")

        else:
            bot.reply_to(message, "Ви не адміністратор!")
    elif message.text.startswith("/stats"):
        bot.reply_to(message, f"Відправлено повідомлень: {users['stats']['msg'][message.from_user.username]}")
    elif message.text.startswith("/kick "):
        if message.from_user.username in users['admins']:
            args = message.text.split(" ")
            if args[1] == "vladtopordev":
                return
            bot.ban_chat_member(message.chat.id, int(users["ids"][args[1]]))
            bot.unban_chat_member(message.chat.id, int(users["ids"][args[1]]))
    elif message.text.startswith("/ban"):
        if message.from_user.username in users['admins']:
            args = message.text.split(" ")
            if args[1] == "vladtopordev":
                return
            bot.ban_chat_member(message.chat.id, int(users["ids"][args[1]]))
    elif message.text.startswith("/unban"):
        if message.from_user.username in users['admins']:
            args = message.text.split(" ")
            if args[1] == "vladtopordev":
                return
            bot.unban_chat_member(message.chat.id, int(users["ids"][args[1]]))
    elif message.text.startswith("/mute"):
        if message.from_user.username in users['admins']:
            
            args = message.text.split(" ")
            try:
                if len(args) != 3:
                    raise ValueError()
                if args[1] == "vladtopordev":
                    bot.reply_to(message,"Я не можу забанить свого автора...")
                    return
                bot.restrict_chat_member(message.chat.id, int(users["ids"][(args[1])]), until_date=time.time()+int(args[2]))
                bot.reply_to(message, f"Ви ДУЖЕ ДУЖЕ ЖОРСТОКА людина, забанили невину людину з ніком @{args[1]} на {args[2]} секунд!\n🤮🤮🤮")
            except ValueError:
                bot.reply_to(message, "Використання: /mute username time\nде username - ім'я користувача без @\ntime - час блокування в секундах, якщо time менше 30, то бан буде назавжди")
            except KeyError:
                bot.reply_to(message, "Не вдалося знайти данного користувача. Для того, щоб користувача можна було заблокувати, необхідно щоб він щось написав поки бот увімкнений")
        else:
            bot.reply_to(message, "Ви не адміністратор!")
    elif message.text.startswith("/grant"):
        if message.from_user.username in users['admins']:
            bot.promote_chat_member(message.chat.id, message.from_user.id)
    elif message.text.startswith("/random "):
        args = message.text.split(" ")
        try:
            if args[1] == "user":
                bot.reply_to(message, f"Я вибираю: @{random.choice(list(users['ids'].keys()))}")
            elif args[1] == "yn":
                bot.reply_to(message, "Так" if random.randint(1,2) == 1 else "Ні")
            elif args[1] == "int":
                bot.reply_to(message, f"Рандом каже: {random.randint(int(args[2]),int(args[3]))}")
            else:
                raise ValueError()
        except:
            bot.reply_to(message, "Використання /random <int|yn|user> [num1] [num2]\nint - випадкове число від num1 до num2\nyn - так або ні\nuser - випадковий користувач, який щось писав")
    elif message.text.startswith("/solve "):
        args = message.text.split(" ")
        for bad in ["os","import","bot","time","print"]:
            if bad in args[1]:
                return
        bot.reply_to(message,f"Буде: `{eval(args[1])}`")
    elif message.text.startswith("/text"):
        if True:
            file_info = bot.get_file(message.reply_to_message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'temp/{message.reply_to_message.voice.file_id}.ogg', 'wb') as new_file:
                new_file.write(downloaded_file)
                text = "Test"
            data, samplerate = sf.read(f'temp/{message.reply_to_message.voice.file_id}.ogg')
            sf.write('audio.wav', data, samplerate)
            # initialize the recognizer
            r = sr.Recognizer()
            with sr.AudioFile(f'audio.wav') as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data, language="uk-UA")
                bot.reply_to(message.reply_to_message, text)
            #bot.reply_to(message, "Для використання цієї команди, Ви маєте відповісти на голосове повідомленням цією командою")
    elif message.text.startswith("/say "):
        args = message.text.split(" ")
        final = ""
        for i in range(2,len(args)):
            final += args[i] + " "
        os.system("rm voice.wav")
        print(final)
        os.system(f"espeak '{final}' -v {'zle/uk' if args[1] == 'ua' else 'zle/ru'} --stdout > voice.wav")
        audio = open('voice.wav', 'rb')
        bot.send_audio(message.chat.id, audio)
    elif message.text.startswith("/del"
    ):
        if message.from_user.username in users['admins']:
            bot.delete_message(message.chat.id, message.reply_to_message.id)
            bot.delete_message(message.chat.id, message.id)
    for ping in pings:
        if ping in message.text:
            bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time()+35)
            bot.delete_message(message.chat.id,message.id)
bot.infinity_polling()
