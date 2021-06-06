import requests
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


token = '1826733806:AAEWbtXKehXyoe0DmlIubGCSBrVYyTkWgwY'
greet_bot = BotHandler(token)
greetings = ('hello', 'hi', 'greetings', 'sup')
# starting_commands = ('/start', '/help')
starting_commands_text = ('start')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        try:
            greet_bot.get_updates(new_offset)

            last_update = greet_bot.get_last_update()

            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            # Commands / part

            if last_chat_text.lower() == '/start':
                greet_bot.send_message(last_chat_id,
                                       '''سلام {} عزیز به ربات ارسال سیگنال های بازار فارکس خوش آمدید. برای فعال سازی اولیه ربات لطفا کلمه ( start ) را وارد نمایید. با تشکر AR™'''.format(last_chat_name))

            elif last_chat_text.lower() == '/help':
                greet_bot.send_message(last_chat_id,
                                       '''نحوه کار ربات:
                                       1: برای فعال سازی ربات شما باید کلمه ( start ) را ارسال نمایید.
                                       2: برای دریافت سیگنال ها شما باید اشتراک تهیه فرمایید. برای تهیه اشتراک به آیدی @AR83051 مراجعه فرمایید.'''.format(last_chat_name))

            #  Text part

            elif last_chat_text.lower() == starting_commands_text:
                greet_bot.send_message(last_chat_id,
                                       '''ربات با موفقیت فعال گردید. لذا برای دریافت سیگنال ها اشتراک تهیه فرمایید. برای تهیه اشتراک به آیدی @AR83051 مراجعه فرمایید. با تشکر AR™''')

            elif last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
                greet_bot.send_message(last_chat_id, 'صبح بخیر  {} عزیز'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
                greet_bot.send_message(last_chat_id, 'ظهر بخیر {} عزیز'.format(last_chat_name))
                today += 1

            elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
                greet_bot.send_message(last_chat_id, 'بعد از ظهر  {} عزیز'.format(last_chat_name))
                today += 1

            # Commands / part ( Unseccful part! )

            elif '/' in last_chat_text.lower():
                greet_bot.send_message(last_chat_id, '''دستور مورد نظر شما قابل اجرا نمی باشد! لطفا دوباره تلاش کنید.''')

            else:
                greet_bot.send_message(last_chat_id,
                                       '''موردی یافت نشد! لطفا دوباره تلاش کنید.''')

            new_offset = last_update_id + 1

        except:
            continue



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()