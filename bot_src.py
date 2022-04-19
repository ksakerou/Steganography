from shutil import ExecError
import telebot
import os

from config import *
from bot_db import Database
from bot_alg import steganize, desteganize



bot = telebot.TeleBot(token)
db = Database(dbname)

@bot.message_handler(content_types='text')
def get_com(msg):
    if msg.text in ['/topic', '/outpic']:
        if msg.text == '/topic':
            db.init_user(msg.from_user.id, 1)
        elif msg.text == '/outpic':
            db.init_user(msg.from_user.id, 2)
        msg = bot.send_message(msg.from_user.id, 'Загрузите изображение.')
        bot.register_next_step_handler(msg, get_pic)
    elif msg.text == '/about':
        bot.send_message(msg.from_user.id, 'хто я')
    else:
        bot.send_message(msg.from_user.id, 'ytn ns')

def get_pic(msg):
    if msg.content_type != 'document':
        bot.send_message(msg.from_user.id,'Ошибка - сообщение не является документом. Попробуйте еще раз.')
    else:
        if not msg.document.file_name[-4:] in ['.png','.jpg']:
            bot.send_message(msg.from_user.id, 'Недопустимое расширение файла. Разрешены только .png и .jpg файлы.')
            db.del_by_id(msg.from_user.id)
        else:
            file_info = bot.get_file(msg.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(msg.from_user.id) + msg.document.file_name[-4:]
            
            with open(picpath + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_pic(msg.from_user.id, file_name)

            user = db.get_by_id(msg.from_user.id)
            if user.status == 1:
                msg = bot.send_message(msg.from_user.id, 'Изображение сохранено. Загрузите файл информации.')
                bot.register_next_step_handler(msg, get_info)
            else:
                try:
                    decoded_file = desteganize(user)
                    bot.send_document(user.id, decoded_file)
                    os.remove(decoded_file.name)
                except Exception:
                    bot.send_message(msg.from_user.id, 'Неизвестная ошибка.')
                db.del_by_id(user.id)

def get_info(msg):
    if msg.content_type != 'document':
        bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является документом. Попробуйте еще раз.')
    else:
        if msg.document.file_name[-4:] in ['.exe','.elf', '.dll'] or msg.document.file_name.find('.') == -1:
            bot.send_message(msg.from_user.id, 'Исполняемые файлы запрещены. Попробуйте другой файл.')
            db.del_by_id(msg.from_user.id)
        else:
            file_info = bot.get_file(msg.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(msg.from_user.id) + msg.document.file_name[msg.document.file_name.find('.'):]

            with open(srcpath + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_src(msg.from_user.id, file_name)

            user = db.get_by_id(msg.from_user.id)

            try:
                incoded_file = steganize(user)
                if incoded_file != None:
                    bot.send_document(msg.from_user.id, incoded_file)
                else:
                    bot.send_message(msg.from_user.id, """Файл информации слишком большой для данной картинки.
                                                        Попробуйте его уменьшить либо увеличить разрешение изображения.""")
            except Exception:
                bot.send_message(msg.from_user.id, 'error')
            db.del_by_id(msg.from_user.id)


bot.polling(non_stop = True, interval = 0)

db.close()