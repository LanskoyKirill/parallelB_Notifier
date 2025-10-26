import os
import pandas as pd
import telebot
import time
import threading
import urllib.request
import json
import random
from AwakeAllTime import keep_alive

def main() -> None:
    """Start the bot."""
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set!")
        return

    bot = telebot.TeleBot(token)

    def send_periodic_messages():
        goodPhrases = ["Ого! Код работает. Срочно нужно звать учёных — это нобелевский уровень!",
                      "Задача решена быстрее, чем Гугл нашёл ответ на Stack Overflow. Это чистая магия.",
                      "Код не только работает, но и выглядит читабельно. Это же уровень программиста-единорога!",
                      "Поздравляю! Баги разбегаются от этого кода, как от огня. Примите эти виртуальные печеньки 🍪.",
                      "Отладка прошла с помощью силы мысли? Потрясающе! Телекинез — вторая профессия.",
                      "Враг повержен, баг повержен, компилятор доволен. Идеальный код!",
                      "Этот код работает так гладко, что его можно показывать как эталон чистого искусства."]
        badSolutions = ["Код работает, и это не сон после 10 часов дебаггинга. Поздравляю с чудом!",
                        "Задача решена! Методом научного (и не очень) тыка.:",
                        "Код работает, но только потому, что ты не проверяешь все случаи. Это не решение, это обман!",
                       "Установлен мировой рекорд по количеству нажатий Ctrl+C / Ctrl+V в поисках ответа.",
                       "Решение найдено! После 100 часов дебаггинга, 5 литров кофе и одной небольшой истерики.",
                       "Переговоры с компилятором успешно завершены, и он, наконец, сдался.",
                       "Задача решена путём случайного удаления точки с запятой и её обратной вставки. Гениально и необъяснимо."]
        badPhrases = ["Код не работает. Это не просто ошибка, это катастрофа.", "Компилятор не понимает тебя. Это не просто баг, это трагедия.",
                      "Кажется, ваш код заключил пакт о ненападении с логикой, и логика победила.",
                      "Даже console.log молчит в недоумении, глядя на это.",
                      "Синий экран смерти увидел ваш код и сам перезагрузился от ужаса.",
                      "Ваша программа работает ровно в двух случаях: при компиляции в воображении и в альтернативной вселенной.",
                      "Кажется, вы обнаружили новый тип бага, который существует вне пространства и времени.",
                      "Кофемашина, глядя на ваши мучения, предложила не кофе, а успокоительное.",
                      "Ваш код выдал такую ошибку, что камера наблюдения в ноутбуке сама вызвала скорую помощь."]
        badSrickers = ["CAACAgIAAxkBAAEBtSZo_hXFBPw6wpjaehjg2oBiPY2gpwACn2UAAqo2uEujE0fTkum0aDYE",      "CAACAgIAAxkBAAEBtSRo_hQ_J1UIdUhIAAFLhO2X_BSY2v4AAtpsAALkp-FLOhDxTlr4-w42BA",
                      "CAACAgIAAxkBAAEBtSpo_hXO-3KfnULapHZ8uSSJsjeFcwACaXgAAuhRoEvbcX6qdtGMbTYE"]
        pastPeople = {}
        
        keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
        keep_alive_thread.start()
        
        while True:
            time.sleep(10)
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
                if key in people:
                    if(pastPeople[key] != people[key]):
                        for i, v in enumerate(people[key]):
                            if pastPeople[key][i] != v:
                                for j, task in enumerate(v):
                                    if pastPeople[key][i][j] != task:
                                        changes.append([key, task, i])
                                        break
            print(changes)
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

    message_thread = threading.Thread(target=send_periodic_messages,
                                      daemon=True)
    message_thread.start()

    print("Bot is starting...")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
