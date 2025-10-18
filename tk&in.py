from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import telebot 

token = "8201590098:AAFv4jws_dKxGFGWQSOEqePbduOPp71FfC0"
SOLO = telebot.TeleBot(token)

@SOLO.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    tiktoki = InlineKeyboardButton('✨TIK TOK✨', callback_data='download_tiktok')
    instagrami = InlineKeyboardButton('✨INSTAGRAM✨', callback_data='download_instagram')
    developerj = InlineKeyboardButton('✨ Dev ✨', url='https://t.me/xv_py')
    channelj = InlineKeyboardButton('Channel ⚠️', url='https://t.me/co_hu')
    markup.add(developerj, channelj)
    markup.add(tiktoki)
    markup.add(instagrami)

    username = message.from_user.username if message.from_user.username else 'unknown_user'
    photo_url = f"https://t.me/{username}"
    namess = f"[{message.from_user.first_name}]({photo_url})"
    text = f"⚠️ اهلا بك عزيزي ✨{namess}✨ في البوت\nاختر أحد الخيارات للمتابعة"
    SOLO.send_photo(message.chat.id, photo_url, caption=text, parse_mode='Markdown', reply_markup=markup)

@SOLO.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'download_instagram':
        if call.message.text:
            SOLO.edit_message_text(text='🔗 | ارسل رابط الفيديو: ', chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            SOLO.send_message(call.message.chat.id, '🔗 | ارسل رابط الفيديو: ')
        SOLO.register_next_step_handler(call.message, download_instagram)

    elif call.data == 'download_tiktok':
        if call.message.text:
            SOLO.edit_message_text(text='🔗 | ارسل رابط الفيديو: ', chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            SOLO.send_message(call.message.chat.id, '🔗 | ارسل رابط الفيديو: ')
        SOLO.register_next_step_handler(call.message, download_tiktok)

def download_instagram(message):
    ag = SOLO.reply_to(message, '⚡ | جارٍ التحميل انتظر . .')
    try:
        msg = message.text
        json_data = {'url': msg}
        response = requests.post('https://insta.savetube.me/downloadPostVideo', json=json_data)

        if response.status_code != 200:
            SOLO.reply_to(message, 'حدث خطأ في الاتصال بالخادم. يرجى المحاولة لاحقًا.')
            return
        
        response_data = response.json()
        
        if 'post_video_url' not in response_data or 'post_video_thumbnail' not in response_data:
            SOLO.reply_to(message, 'رابط غير صالح')
            return
        
        vd = response_data['post_video_url']
        thumb = response_data['post_video_thumbnail']
        bt = f"- @{SOLO.get_me().username} ."        
        SOLO.send_video(message.chat.id, vd, caption='🎉تم تحميل الفيديو بنجاح🎉\nDEV🔥@xv_py\nCH🔥@CO_HU\nBOT🔥' + bt, reply_to_message_id=message.message_id)
    except Exception as e:
        SOLO.reply_to(message, 'حدث خطأ أثناء تحميل الفيديو. يرجى المحاولة مرة أخرى.')
        print(f"Error: {e}")

def download_tiktok(message):
    ag = SOLO.reply_to(message, '⚡ | جارٍ التحميل انتظر . .')
    video_url = message.text
    try:
        request_url = f"https://www.tikwm.com/api/?url={video_url}"
        response = requests.get(request_url)
        
        if response.status_code == 200:
            response_data = response.json()
            if 'data' in response_data and 'play' in response_data['data']:
                video_link = response_data['data']['play']
                bt = f"- @{SOLO.get_me().username} ."
                SOLO.send_video(message.chat.id, video_link, caption='🎉تم تحميل الفيديو بنجاح🎉\nDEV🔥@xv_py\nCH🔥@CO_HU\nBOT🔥' + bt)
            else:
                SOLO.reply_to(message, "لم أتمكن من جلب الفيديو، تحقق من الرابط.")
        else:
            SOLO.reply_to(message, "خطأ في استجابة الخادم. حاول لاحقاً.")

    except requests.exceptions.RequestException as e:
        SOLO.reply_to(message, "حدث خطأ في الشبكة. حاول مجدداً.")
        print(f"Network Error: {e}")
    except Exception as e:
        SOLO.reply_to(message, "حدث خطأ أثناء تحميل الفيديو. حاول مجدداً.")
        print(f"Error: {e}")

SOLO.polling()