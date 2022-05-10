import telebot
import os

from config import *
from bot_db import Database, copyfile
from bot_alg import steganize, desteganize, genpic



bot = telebot.TeleBot(token)
db = Database(dbname)

@bot.message_handler(content_types = content_types_any)
def get_com(msg):
    if msg.content_type == 'text':
        if msg.text == '/topic':
            db.init_user(msg.from_user.id, msg.text)
            msg = bot.send_message(msg.from_user.id, 'Загрузите изображение нет блин аудио или напишите /example, чтобы использовать картинку с нашим лого.')
            bot.register_next_step_handler(msg, get_pic)

        elif msg.text == '/outpic':
            db.init_user(msg.from_user.id, msg.text)
            msg = bot.send_message(msg.from_user.id, 'Загрузите изображение нет блин аудио.')
            bot.register_next_step_handler(msg, get_stor)

        elif msg.text == '/about':
            bot.send_message(msg.from_user.id, 'хто я и все кредитс типа бота создал @kaaamoon лил воду @tikto')

        elif msg.text == '/die' and msg.from_user.id == father_id:
            #reopen console where you start bot
            bot.stop_polling() 
        else:
            bot.send_message(msg.from_user.id, 'тут будет ссылка на инструкцию для дегенератов и других проверяющих')
    else:
        bot.send_message(msg.from_user.id, 'тут будет ссылка на инструкцию для дегенератов и других проверяющих')


def get_stor(msg):
    if msg.content_type == 'text' and msg.text == '/back':
        bot.send_message(msg.from_user.id, 'краткая инструкция для тупых')
        db.del_by_id(msg.from_user.id)

    elif msg.content_type != 'document':
        msg = bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является документом. Попробуйте еще раз или напишите /back для возвращения в основное меню')
        bot.register_next_step_handler(msg, get_stor)

    else:
        fname = msg.document.file_name

        if fname.find('.') == -1 or fname[fname.rfind('.'):] != '.png':
            msg = bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является файлом формата .png. Попробуйте еще раз или напишите /back для возвращения в основное меню')
            bot.register_next_step_handler(msg, get_stor)

        else:
            file_info = bot.get_file(msg.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(msg.from_user.id) + '.png'

            with open(picpath + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_pic(msg.from_user.id, file_name)

            user = db.get_by_id(msg.from_user.id)
            send_info(user)
            db.del_by_id(user.id)


def send_info(user):
    try:
        decoded_file = desteganize(user)
        if decoded_file == None:
            bot.send_message(user.id, 'Ошибка - файл не является носителем.')
        else:
            db.add_src(user.id, decoded_file.name[decoded_file.name.rfind('/') + 1:])
            bot.send_document(user.id, decoded_file)

    except Exception as e:
        bot.send_message(user.id, f'Ошибка - {e}')



def get_pic(msg):
    if msg.content_type == 'text' and msg.text == '/back':
        bot.send_message(msg.from_user.id, 'краткая инструкция для тупых')
        db.del_by_id(msg.from_user.id)
    
    elif msg.content_type == 'text' and msg.text == '/example':
        bot.send_message(msg.from_user.id, 'Введите размер изображения в формате "ШИРИНА ВЫСОТА" через пробел.')
        bot.register_next_step_handler(msg, get_size)

    elif msg.content_type not in ['photo', 'document']:
        msg = bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является изображением. Попробуйте еще раз или напишите /back для возвращения в основное меню.')
        bot.register_next_step_handler(msg, get_pic)

    elif msg.content_type == 'photo':
        file_info = bot.get_file(msg.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = str(msg.from_user.id) + '.jpg'

        with open(picpath + file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        db.add_pic(msg.from_user.id, file_name)

        msg = bot.send_message(msg.from_user.id, 'Изображение сохранено. Загрузите файл информации.')
        bot.register_next_step_handler(msg, get_info)

    elif msg.content_type == 'document':
        fname = msg.document.file_name

        if fname[fname.rfind('.'):].lower() not in ['.jpg', '.png', '.jpeg']:
            bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является изображением. Попробуйте еще раз или напишите /back для возвращения в основное меню.')
            bot.register_next_step_handler(msg, get_pic)

        else:
            file_info = bot.get_file(msg.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(msg.from_user.id) + fname[fname.rfind('.'):]

            with open(picpath + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_pic(msg.from_user.id, file_name)

            msg = bot.send_message(msg.from_user.id, 'Изображение сохранено. Загрузите файл информации.')
            bot.register_next_step_handler(msg, get_info)


def get_size(msg):
    if msg.content_type != 'text':
        msg = bot.send_message(msg.from_user.id, 'Ошибка - некорректный размер картинки. Введите валидный размер либо напишите /back для возвращения в основное меню.')
        bot.register_next_step_handler(msg, get_size)

    elif msg.text == '/back':
        bot.send_message(msg.from_user.id, 'краткая инструкция для тупых')
        db.del_by_id(msg.from_user.id)
    
    else:
        try:
            s = msg.text.split(' ')
            width, height = int(s[0]), int(s[1]) 

            if width <= 0 or height <= 0 or width*height > 2**25:
                msg = bot.send_message(msg.from_user.id, 'Ошибка - некорректный размер картинки. Введите валидный размер либо напишите /back для возвращения в основное меню.')
                bot.register_next_step_handler(msg, get_size)
            
            else:
                file_name = str(msg.from_user.id) + ex_pic[ex_pic.find('.'):]
                
                genpic(file_name, (width, height))
                db.add_pic(msg.from_user.id, file_name)
                
                msg = bot.send_message(msg.from_user.id, 'Изображение подготовлено. Загрузите файл информации или напишите /example, чтобы попытаться загрузить в качестве информации шикарного пиксельного динозавра')
                bot.register_next_step_handler(msg, get_info)

        except Exception as e:
            msg = bot.send_message(msg.from_user.id, f'Ошибка - {e}. Введите валидный размер либо напишите /back для возвращения в основное меню.')
            bot.register_next_step_handler(msg, get_size)


def get_info(msg):
    if msg.content_type == 'text' and msg.text == '/back':
        bot.send_message(msg.from_user.id, 'краткая инструкция для тупых')
        db.del_by_id(msg.from_user.id)

    elif msg.content_type == 'text' and msg.text == '/example':
        with open(srcpath + ex_src, 'rb') as fex:
            bin_ex = fex.read()
        
        file_name = str(msg.from_user.id) + ex_src[ex_src.find('.'):]
        
        with open(srcpath + file_name, 'wb') as fout:
            fout.write(bin_ex)
        db.add_src(msg.from_user.id, file_name)
        
        user = db.get_by_id(msg.from_user.id)
        send_stor(user)
        db.del_by_id(user.id)


    elif msg.content_type != 'document':
        msg = bot.send_message(msg.from_user.id, 'Ошибка - сообщение не является документом. Попробуйте еще раз или напишите /back для возвращения в основное меню.')
        bot.register_next_step_handler(msg, get_info)

    else:
        fname = msg.document.file_name

        if fname.find('.') == -1 or fname[-4:] in ['.exe','.elf', '.dll']:
            msg = bot.send_message(msg.from_user.id, 'Исполняемые файлы запрещены к использованию на территории РФ. Попробуйте другой файл или напишите /back для возвращения в основное меню.')
            bot.register_next_step_handler(msg, get_info)

        else:
            file_info = bot.get_file(msg.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = str(msg.from_user.id) + fname[fname.find('.'):]

            with open(srcpath + file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_src(msg.from_user.id, file_name)

            user = db.get_by_id(msg.from_user.id)
            send_stor(user)
            db.del_by_id(user.id)

def send_stor(user):
    try:
        incoded_file = steganize(user)
        
        if incoded_file != None:
            bot.send_document(user.id, incoded_file)
            copyfile(incoded_file.name[:incoded_file.name.rfind('/') + 1], incoded_file.name[incoded_file.name.rfind('/') + 1:])
            os.remove(incoded_file.name)

        else:
            bot.send_message(user.id, 'Файл информации слишком большой.')
            
    except Exception as e:
        bot.send_message(user.id, f'Ошибка - {e}')

bot.polling(non_stop = True, interval = 0)

db.close()