import threading

import telebot
from telebot import types
from data import  questions, answers
from Phrases import  sl
from random import  randint

TOKEN = "977114700:AAEXR46cIpw4D5hCxDiVTl2EWzNJwCKyY5w"
bot = telebot.TeleBot(TOKEN)

# Список задач и правильных ответов
# QUESTIONS = [
#     ("Сколько будет 2 + 2?", 4),
#     ("Чему равен корень из 16?", 4),
#     ("Сколько сторон у квадрата?", 4),
#     ("Сколько градусов в прямом угле?", 90),
#     ("Сколько планет в Солнечной системе?", 8),
#     ("Сколько материков на Земле?", 7),
#     ("Сколько часов в сутках?", 24),
# ]

QUESTIONS = []
for i in range(1, 8):
    QUESTIONS.append((questions[i], answers[i]))


# Словарь для хранения прогресса пользователей
user_progress = {}
active_users = set()

@bot.message_handler(commands=['start'])
def start(message):
    photo = f'bender{randint(1, 4)}.jpg'
    user_id = message.from_user.id
    user_progress[user_id] = 0  # Начинаем с первой задачи
    active_users.add(user_id)
    # bot.send_message(
    #     user_id,
    #     f"Вы – несчастный ученик, который по неосторожности заключил сделку с Великим Комбинатором Остапом Бендером. Теперь вы вынуждены пройти серию интеллектуальных испытаний, чтобы вернуть себе свободу (и свою последнюю мелочь). Бендер – ваш ведущий, судья и безжалостный комментатор."
    # )
    with open(photo, "rb") as photo:
        bot.send_photo(user_id, photo, caption=f"Вы – несчастный ученик, который по неосторожности заключил сделку с Великим Комбинатором Остапом Бендером. Теперь вы вынуждены пройти серию интеллектуальных испытаний, чтобы вернуть себе свободу (и свою последнюю мелочь). Бендер – ваш ведущий, судья и безжалостный комментатор.")
    bot.send_message(user_id, f'{sl['Вступление'][randint(0, 6)]}\n\n{QUESTIONS[0][0]}')

def send_random_phrase():
    threading.Timer(300, send_random_phrase).start()  # Запуск каждые 5 минут
    for user_id in active_users:
        bot.send_message(user_id, f'{sl['Поддержание атмосферы'][randint(0, 6)]}')

@bot.message_handler(func=lambda message: True)
def answer_question(message):
    photo = f'bender{randint(1, 4)}.jpg'
    user_id = message.from_user.id
    print(message.from_user.id, message.from_user.first_name, message.text)
    if user_id not in user_progress:
        bot.send_message(user_id, f"Если хочешь еще раз сыграть, введи команду /start.")
        return
        #user_progress[user_id] = 0

    question_index = user_progress[user_id]

    try:
        user_answer = message.text
    except ValueError:
        bot.send_message(user_id, f"{sl['Реакция на неправильный ответ'][randint(0, 6)]}")
        return

    correct_answer = QUESTIONS[question_index][1]

    if user_answer == correct_answer:
        user_progress[user_id] += 1

        if user_progress[user_id] < len(QUESTIONS):
            with open(photo, "rb") as photo:
                bot.send_photo(user_id, photo, caption=f"{sl['Реакция на правильный ответ'][randint(0, 6)]}")
            #bot.send_message(user_id, f"{sl['Реакция на правильный ответ'][randint(0, 6)]}")
            bot.send_message(user_id, f"{sl['Задания'][user_progress[user_id]]}\n\n{QUESTIONS[user_progress[user_id]][0]}")
        else:
            bot.send_message(user_id, f"{sl['Завершение'][randint(0, 6)]}")
            del user_progress[user_id]  # Сброс прогресса
            bot.send_message(user_id, f"Если хочешь еще раз сыграть, введи команду /start.")
    else:
        bot.send_message(user_id, f"{sl['Реакция на неправильный ответ'][randint(0, 6)]}")

send_random_phrase()

if __name__ == "__main__":
    bot.polling(none_stop=True)
