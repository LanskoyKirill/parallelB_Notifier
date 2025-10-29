import os
import pandas as pd
import telebot
import time
import threading
import urllib.request
import json
import random
from AwakeAllTime import keep_alive
from phrases import goodPhrases, badSolutions, badPhrases, badSrickers

def main() -> None:
    """Start the bot."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set!")
        return

    bot = telebot.TeleBot(token)

    def send_periodic_messages():
        pastPeople = {}
        
        # Start keep_alive server in a separate thread
        #keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
        #keep_alive_thread.start()
        
        while True:
            time.sleep(120)
            urlOfRank = "https://ej-3.t-edu.tech/standings-data/b2025"
            data = []
            with urllib.request.urlopen(urlOfRank) as url:
                data = json.loads(url.read().decode())

            contests = data.get('contests', [])
            standings = data.get('standings', [])
            nameOfTasks = [item['name'] + " " + problem['short'] for item in contests for problem in item['problems']]
            people = {item['name']: [problem['tasks'] for problem in item['per_contests']] for item in standings}
            changes = []
            for key in pastPeople:
                if key in people and key != "Ланской Кирилл":
                    if pastPeople[key] != people[key]:
                        for i, v in enumerate(people[key]):
                            if pastPeople[key][i] != v:
                                for j, task in enumerate(v):
                                    try:
                                        if pastPeople[key][i][j] != task and key != 0:
                                            changes.append([key, task, i])
                                            break
                                    except Exception:
                                        pass
            str_val = ""
            if len(changes) > 0:
                a = changes[random.randint(0, len(changes) - 1)]
                if a[1] > 0:
                    str_val = f"{a[0]} смог(-ла) решить задачу {nameOfTasks[a[2]]} за {abs(a[1])}"
                    if a[1] % 10 == 1:
                        str_val += " попытку!"
                    elif a[1] % 10 in [2, 3, 4]:
                        str_val += " попытки!"
                    else:
                        str_val += " попыток!"
                    if a[1] == 1 and random.randint(0, 5) == 0:
                        str_val += "\nПоздравляю! Код скомпилировался с первого раза. Неужели была заключена сделка с компилятором?"
                    elif a[1] <= 5:
                        str_val += "\n" + goodPhrases[random.randint(0, len(goodPhrases) - 1)]
                    else:
                        str_val += "\n" + badSolutions[random.randint(0, len(badSolutions) - 1)]
                else:
                    str_val = f"{a[0]} не смог(-ла) решить задачу {nameOfTasks[a[2]]} за {abs(a[1])}"
                    if abs(a[1]) % 10 == 1:
                        str_val += " попытку!"
                    elif abs(a[1]) % 10 in [2, 3, 4]:
                        str_val += " попытки!"
                    else:
                        str_val += " попыток!"
                    str_val += "\n" + badPhrases[random.randint(0, len(badPhrases) - 1)]
                bot.send_message(-1003237662697, str_val)
                if(a[1] > 0 and random.randint(0, 3) == 0):
                    bot.send_sticker(-1003237662697, "CAACAgIAAxkBAAEBtSJo_hQ5EiZL5UOwGE12yZjL9zbrbAACj2oAAvMOSUghNXtEimGGpzYE")
                if(a[1] < 0 and random.randint(0, 3) == 0):
                    bot.send_sticker(-1003237662697, badSrickers[random.randint(0, len(badSrickers) - 1)])
                print(str_val)
            pastPeople = people

    # Start periodic message sender in a separate thread
    message_thread = threading.Thread(target=send_periodic_messages,
                                      daemon=True)
    message_thread.start()

    print("Bot is starting...")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
