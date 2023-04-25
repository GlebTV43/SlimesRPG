import ast
import re
import random
import string
import sqlite3

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def exp_to_level(exp, fl=False):
    b1 = 100
    q = 1.25
    tmp = 0
    ans = 0
    for x in range(1000):
        tmp += b1 * q ** x
        if tmp >= exp:
            ans = x
            break
    else:
        return int(1e9)
    if fl:
        return ans, int(tmp - exp)
    return ans


def money_coef(exp):
    level = exp_to_level(exp)
    ans = 0
    for x in range(level):
        ans += int(8 * x ** 2.5 + 100)
    return ans


def get_profile(cur_user, source_mid):
    data = cur_user.execute(
        f"""SELECT User_Name, Rating, Experience, 
                            Money, Health_Points, Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                            E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                            C_Attack, F_Attack, M_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
    return f"""Имя пользователя: {data[0]}
               Очки рейтинга: {data[1]:,}
               Уровень: {exp_to_level(data[2])} Монеты: {data[3]:,}
               Опыта до следующего уровня: {exp_to_level(data[2], fl=True)[1]:,}
               Здоровье: {data[4]}/{data[5]}
               Базовая атака: {data[6]:.2f} Базовая защита: {data[7]:.2f}
               Критическая атака: {data[8]:.2f} Шанс критической атаки {data[9] * 100:.2f}%
               Физические характеристики:
               Защита: {data[10]:.2f} Атака: {data[14]:.2f}
               Криогенные характеристики:
               Защита: {data[11]:.2f} Атака: {data[15]:.2f}
               Огненные характеристики:
               Защита: {data[12]:.2f} Атака: {data[16]:.2f}
               Магические характеристики:
               Защита: {data[13]:.2f} Атака: {data[17]:.2f}"""


def fight_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Физическая атака', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Криогенная атака', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Огненная атака', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Магическая атака', color=VkKeyboardColor.SECONDARY)

    return keyboard


def advanced_shop_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Физические характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Криогенные характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(f'Огненные характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Магические характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    return keyboard


def advanced_mini_shop_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Атака', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Защита', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    return keyboard


def base_shop_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Базовый урон', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Базовая защита', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(f'Максимальное здоровье', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Критический урон', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Шанс критического урона', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    return keyboard


def shop_keyboard(cur_user, source_mid):
    data = cur_user.execute(
        f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                 FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
    cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
    if data[3] / data[2] == 1:
        cost = 0
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Базовые характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Дополнительные характеристики', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(f'Лечение {cost:,} монет', color=VkKeyboardColor.SECONDARY)
    # keyboard.add_button('Ограничения', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Как это работает?', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    return keyboard


def main_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Как играть', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Настройки', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Сражаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button("Показатели", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Улучшения", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Рейтинг", color=VkKeyboardColor.POSITIVE)

    # keyboard.add_button("Бонусы", color=VkKeyboardColor.SECONDARY)
    return keyboard


def settings_keyboard():
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Сменить имя', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Сбросить имя пользователя', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Подвязать аккаунт Telegram', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Получить мой ID в VK', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Уникальный ключ доступа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Перегенерировать уникальный ключ доступа', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Отвязать аккаунт Telegram', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

    return keyboard


# UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='Users'

def main():
    con_user = sqlite3.connect("users.db")
    cur_user = con_user.cursor()
    with open('vk_token.txt', 'r') as f:
        token = f.readline()
        f.close()
    vk_session = vk_api.VkApi(
        token=token)
    while True:
        try:
            longpoll = VkBotLongPoll(vk_session, "219948677")
            for event in longpoll.listen():
                vk = vk_session.get_api()
                if hasattr(event, 'source_act') and event.source_act == 'chat_invite_user':
                    source_mid = event.source_mid

                if event.type == VkBotEventType.MESSAGE_NEW:
                    source_mid = event.obj.message['from_id']
                    message = event.obj.message['text']
                    status = cur_user.execute(f"SELECT Status FROM Users WHERE VK_ID = {source_mid}").fetchall()
                    try:
                        status = status[0][0]
                    except:
                        status = -10
                    if status == -10:
                        keyboard = VkKeyboard(one_time=True)

                        keyboard.add_button('Новый аккаунт', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('Подвязать', color=VkKeyboardColor.POSITIVE)

                        vk.messages.send(user_id=source_mid,
                                         message="Вам необходимо зарегистрироваться",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        cur_user.execute(f"INSERT INTO Users(VK_ID) VALUES({source_mid})")
                        cur_user.execute(f"UPDATE Users SET Status = -1 WHERE VK_ID = {source_mid}")
                        con_user.commit()
                        continue
                    elif status in [141]:
                        keyboard = main_keyboard()
                        vk.messages.send(user_id=source_mid,
                                         message="Выберите: ",
                                         keyboard=keyboard.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        cur_user.execute(
                            f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                        con_user.commit()
                        continue
                    elif status == -1:
                        if message == 'Новый аккаунт':
                            user_get = vk.users.get(user_ids=(event.obj.message['from_id']))
                            user_get = user_get[0]
                            first_name = user_get['first_name']
                            last_name = user_get['last_name']
                            while True:
                                lenth = 100
                                tmp = cur_user.execute(f"SELECT User_ID FROM Users WHERE VK_ID = {source_mid}").fetchall()[0][
                                    0]
                                unique_id = str(source_mid) + str(tmp) + id_generator(lenth - len(str(source_mid) + str(tmp)))
                                if cur_user.execute(f"SELECT * FROM Users WHERE Unique_ID = '{unique_id}'").fetchall():
                                    continue
                                cur_user.execute(f"UPDATE Users SET Unique_ID = '{unique_id}' WHERE VK_ID = {source_mid}")
                                cur_user.execute(
                                    f"UPDATE Users SET User_Name = '{first_name + ' ' + last_name}' WHERE VK_ID = {source_mid}")
                                cur_user.execute(
                                    f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                                con_user.commit()
                                break
                            con_user.commit()
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Успех', color=VkKeyboardColor.PRIMARY)

                            vk.messages.send(user_id=source_mid,
                                             message=f"Вы успешно зарегистрировались!\n"
                                                     f"Ваше внутриигровое имя: {first_name + ' ' + last_name}\n "
                                                     f"Вы можете его изменить в настройках",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif message == 'Подвязать':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
                            vk.messages.send(user_id=source_mid,
                                             message=f"Введите ваш уникальный ключ доступа"
                                                     f"\nВаш ID в VK: {source_mid}",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = -2 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                        else:
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Новый аккаунт', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подвязать', color=VkKeyboardColor.POSITIVE)

                            vk.messages.send(user_id=source_mid,
                                             message="Вам необходимо зарегистрироваться",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(f"UPDATE Users SET Status = -1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status == -2:
                        if message == 'Назад':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Новый аккаунт', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подвязать', color=VkKeyboardColor.POSITIVE)

                            vk.messages.send(user_id=source_mid,
                                             message="Вам необходимо зарегистрироваться",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(f"UPDATE Users SET Status = -1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                        else:
                            cur_user.execute(f"UPDATE Users SET VK_ID_REG = {source_mid} WHERE Unique_ID = '{message}'")
                            con_user.commit()
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Новый аккаунт', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('Подвязать', color=VkKeyboardColor.POSITIVE)

                            vk.messages.send(user_id=source_mid,
                                             message="Вам необходимо подтвердить привязку из акканта Telegram",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Вам необходимо зарегистрироваться",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(f"UPDATE Users SET Status = -1 WHERE VK_ID = {source_mid}")
                            con_user.commit()

                    elif status == 1:
                        if message == 'Как играть':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            vk.messages.send(user_id=source_mid,
                                             message="Правила игры:\nВас атакуют монстры, единственное, что вы можете сделать, это смириться и приспособиться к этому, улучшая свои характеристики. За каждого выигрыного слайма вы получаете рейтинг. \nСоревнуйтесь с друзьями, проверяя свой рейтинг на сайте игры.",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))

                            cur_user.execute(
                                f"UPDATE Users SET Status = 11 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Показатели':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Улучшения', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Как играть', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            cur_user.execute(
                                f"UPDATE Users SET Status = 12 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=get_profile(cur_user, source_mid),
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif message == 'Рейтинг':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Что такое Очки рейтинга?', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_line()
                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            cur_user.execute(
                                f"UPDATE Users SET Status = 13 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            all_rating = cur_user.execute(f"SELECT VK_ID, TG_ID, Rating FROM Users").fetchall()
                            print(all_rating)
                            all_rating.sort(key=lambda x: x[2], reverse=True)
                            current_row = cur_user.execute(
                                f"SELECT VK_ID, TG_ID, Rating FROM Users WHERE VK_ID = {source_mid}").fetchall()
                            rating = all_rating.index(current_row[0])
                            vk.messages.send(user_id=source_mid,
                                             message=f"Ваше положение в общем рейтинге: {rating + 1} с Очками Рейтинга: {current_row[0][2]}",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Настройки':
                            keyboard = settings_keyboard()
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Улучшения':
                            keyboard = shop_keyboard(cur_user, source_mid)
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                 FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Улучшения
                                                         Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                         Здоровье: {data[2]:,}/{data[3]:,}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 15 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                        elif message == "Сражаться":
                            keyboard = fight_keyboard()
                            data = cur_user.execute(
                                f"""SELECT User_Name, Rating, Experience, 
                                            Money, Health_Points, Max_Health_Points, 
                                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                            E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                            C_Attack, F_Attack, M_Attack FROM Users 
                                            WHERE VK_ID = {source_mid}""").fetchall()[0]
                            level = exp_to_level(data[2])
                            base = cur_user.execute(f"""SELECT * FROM Slimes WHERE Enemy_Level <= {level}""").fetchall()
                            enemy = random.choice(base)
                            cur_user.execute(f"""UPDATE Users SET Current_Enemy_ID = {enemy[0]} WHERE VK_ID = {source_mid}""")
                            cur_user.execute(
                                f"""UPDATE Users SET Current_Enemy_HP = {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} WHERE VK_ID = {source_mid}""")
                            cur_user.execute(
                                f"""UPDATE Users SET Current_Enemy_Max_HP = {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} WHERE VK_ID = {source_mid}""")
                            cur_user.execute(
                                f"""UPDATE Users SET Current_Enemy_Attack = {max(enemy[4], enemy[4] * 0.01 ** (0.5 * level))} WHERE VK_ID = {source_mid}""")
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Обнаружен враг {enemy[1]}
                                                        Здоровье: {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))}/{max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))}
                                                        Базовый урон: {max(enemy[4], enemy[4] * 0.01 ** (0.5 * level)):.2f}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(f"""UPDATE Users SET Status = 60 WHERE VK_ID = {source_mid}""")
                            con_user.commit()
                        else:
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                    elif status == 11:
                        if message == 'Назад':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        else:
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            vk.messages.send(user_id=source_mid,
                                             message="Правила игры:\nВас атакуют монстры, единственное, что вы можете сделать, это смириться и приспособиться к этому, улучшая свои характеристики. За каждого выигрыного слайма вы получаете рейтинг. \nСоревнуйтесь с друзьями, проверяя свой рейтинг на сайте игры.",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))

                            cur_user.execute(
                                f"UPDATE Users SET Status = 11 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status == 101:
                        if message == 'Назад':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Улучшения', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Как играть', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            cur_user.execute(
                                f"UPDATE Users SET Status = 12 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=get_profile(cur_user, source_mid),
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif message == 'В главное меню':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        else:
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_line()
                            keyboard.add_button('В главное меню', color=VkKeyboardColor.SECONDARY)
                            vk.messages.send(user_id=source_mid,
                                             message="Правила игры:\nВас атакуют монстры, единственное, что вы можете сделать, это смириться и приспособиться к этому, улучшая свои характеристики. За каждого выигрыного слайма вы получаете рейтинг. \nСоревнуйтесь с друзьями, проверяя свой рейтинг на сайте игры.",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))

                            cur_user.execute(
                                f"UPDATE Users SET Status = 101 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status == 12:
                        if message == 'Назад':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Как играть':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_line()
                            keyboard.add_button('В главное меню', color=VkKeyboardColor.SECONDARY)
                            vk.messages.send(user_id=source_mid,
                                             message="Правила игры:\nВас атакуют монстры, единственное, что вы можете сделать, это смириться и приспособиться к этому, улучшая свои характеристики. За каждого выигрыного слайма вы получаете рейтинг. \nСоревнуйтесь с друзьями, проверяя свой рейтинг на сайте игры.",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))

                            cur_user.execute(
                                f"UPDATE Users SET Status = 101 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Улучшения':
                            keyboard = shop_keyboard(cur_user, source_mid)
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                     FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Улучшения
                                                                             Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                                             Здоровье: {data[2]:,}/{data[3]:,}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 15 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                        else:
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Улучшения', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Как играть', color=VkKeyboardColor.SECONDARY)
                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            cur_user.execute(
                                f"UPDATE Users SET Status = 12 WHERE VK_ID = {source_mid}")
                            # data = cur_user.execute(
                            #     f"""SELECT User_Name, Rating, Experience,
                            #     Money, Health_Points, Max_Health_Points,
                            #     Base_Attack, Base_Shield, Critical_Attack, Critical_Chance,
                            #     E_Shield, C_Shield, F_Shield, M_Shield, E_Attack,
                            #     C_Attack, F_Attack, M_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=get_profile(cur_user, source_mid),
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                    elif status == 13:
                        if message == 'Что такое Очки рейтинга?':
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)
                            vk.messages.send(user_id=source_mid,
                                             message="С помощью Очков рейтинга, получаемого при победе в бою, вы повышаете свое место в общем рейтинге игроков.\nОбщий рейтинг: http://185.185.71.200:8080",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif message == 'Назад':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status == 14:
                        
                        if message == 'Сменить имя':
                            vk.messages.send(user_id=source_mid,
                                             message="Введите свое имя",
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 214 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Сбросить имя пользователя':
                            keyboard = settings_keyboard()
                            user_get = vk.users.get(user_ids=(event.obj.message['from_id']))
                            user_get = user_get[0]
                            first_name = user_get['first_name']
                            last_name = user_get['last_name']
                            cur_user.execute(
                                f"UPDATE Users SET User_Name = '{first_name + ' ' + last_name}' WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Имя пользователя успешно изменено на {first_name + ' ' + last_name}",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Уникальный ключ доступа':
                            keyboard = settings_keyboard()
                            code = cur_user.execute(f"SELECT Unique_ID FROM Users WHERE VK_ID = {source_mid}").fetchall()[0][
                                0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"Ваш уникальный ключ доступа для привязки аккаунта Telegram:"
                                                     f" \n{code}\nНиктому не сообщайте его!",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Перегенерировать уникальный ключ доступа':
                            while True:
                                lenth = 100
                                tmp = cur_user.execute(f"SELECT User_ID FROM Users WHERE VK_ID = {source_mid}").fetchall()[0][
                                    0]
                                unique_id = str(source_mid) + str(tmp) + id_generator(lenth - len(str(source_mid) + str(tmp)))
                                if cur_user.execute(f"SELECT * FROM Users WHERE Unique_ID = '{unique_id}'").fetchall():
                                    continue
                                cur_user.execute(f"UPDATE Users SET Unique_ID = '{unique_id}' WHERE VK_ID = {source_mid}")
                                con_user.commit()
                                break
                            keyboard = settings_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Ваш уникальный ключ доступа был пересоздан"
                                                     f" \nНиктому не сообщайте его!",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Получить мой ID в VK':
                            keyboard = settings_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Ваш ID аккаунта VK: {source_mid}\n При подтверждении привязки "
                                                     f"Telegram аккаунта к VK "
                                                     f"обязательно сравните этот ID VK с предложенным ID VK в Telegram боте\n"
                                                     f"При обнаружении различия, не подтверждая это объединение, повторного "
                                                     f"проведите процедуру привязки аккаунтов",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif message == 'Подвязать аккаунт Telegram':
                            tg_id_reg = cur_user.execute(f"SELECT TG_ID_REG FROM Users WHERE "
                                                         f"VK_ID = {source_mid}").fetchall()[0][0]
                            if tg_id_reg is not None:
                                keyboard = VkKeyboard(one_time=True)

                                keyboard.add_button('Подтвердить', color=VkKeyboardColor.POSITIVE)
                                keyboard.add_button('Отклонить', color=VkKeyboardColor.NEGATIVE)
                                keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Аккаунт Telegram с ID {tg_id_reg} хочет подвязаться к вашему "
                                                         f"профилю.\n"
                                                         f"Сравните данный ID с ID вашего аккаунта Telegram. "
                                                         f"(Его вы можете получить также через нашего бота в Telegram)\n"
                                                         f"Если вы этого не делали или ID не совпали, "
                                                         f"то рекомендуем немедленно отклонить запрос "
                                                         f"и перегенерировать 'Уникальный ключ доступа' в настройках",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                cur_user.execute(
                                    f"UPDATE Users SET Status = 3114 WHERE VK_ID = {source_mid}")
                                con_user.commit()
                            else:
                                keyboard = settings_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Не обнаружено входящих запросов",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message="Настройки: ",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == "Отвязать аккаунт Telegram":
                            keyboard = settings_keyboard()
                            tg_id = cur_user.execute(f"SELECT TG_ID FROM Users WHERE "
                                                     f"VK_ID = {source_mid}").fetchall()[0][0]
                            if tg_id:
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Эта операция не производится автоматически для вашей же безопасности."
                                                         "Вы можете оставить заявку на:"
                                                         "Email: qwerty@mail.ru""",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message="Настройки: ",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Не обнаружено подвязанной учетной записи Telegram""",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message="Настройки: ",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        else:
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status == 214:
                        if len(message) > 48:
                            keyboard = settings_keyboard()
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message="Имя пользователя слишком большое",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif len(message) < 5:
                            keyboard = settings_keyboard()
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message="Имя пользователя слишком короткое",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif any(char in ".,:;!_*-+()/#¤%&?)" for char in message):
                            keyboard = settings_keyboard()
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message="Имя пользователя не должно содержать .,:;!_*-+()/#¤%&?",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            keyboard = settings_keyboard()
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            cur_user.execute(
                                f"UPDATE Users SET User_Name = '{message}' WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Имя пользователя успешно изменено на {message}",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                    elif status == 3114:
                        tg_id_reg = cur_user.execute(f"SELECT TG_ID_REG FROM Users WHERE "
                                                     f"VK_ID = {source_mid}").fetchall()[0][0]
                        if message == 'Назад':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Подтвердить':
                            cur_user.execute(f"DELETE FROM Users WHERE TG_ID = '{tg_id_reg}'")
                            cur_user.execute(
                                f"UPDATE Users SET TG_ID = '{tg_id_reg}' WHERE VK_ID = {source_mid}")
                            cur_user.execute(
                                f"UPDATE Users SET TG_ID_REG = NULL WHERE VK_ID = {source_mid}")
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            keyboard = settings_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Telegram аккаунт с ID {tg_id_reg} и VK аккаунт с ID {source_mid} "
                                                     f"теперь объединены",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif message == 'Отклонить':
                            cur_user.execute(
                                f"UPDATE Users SET TG_ID_REG = NULL WHERE VK_ID = {source_mid}")
                            cur_user.execute(
                                f"UPDATE Users SET Status = 14 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            keyboard = settings_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Запрос на добавление Telegram аккаунта был отклонен",
                                             random_id=random.randint(0, 2 ** 64))
                            vk.messages.send(user_id=source_mid,
                                             message="Настройки: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            keyboard = VkKeyboard(one_time=True)

                            keyboard.add_button('Подтвердить', color=VkKeyboardColor.POSITIVE)
                            keyboard.add_button('Отклонить', color=VkKeyboardColor.NEGATIVE)
                            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
                            vk.messages.send(user_id=source_mid,
                                             message=f"Аккаунт Telegram с ID {tg_id_reg} хочет подвязаться к вашему "
                                                     f"профилю.\n"
                                                     f"Сравните данный ID с ID вашего аккаунта Telegram. "
                                                     f"(Его вы можете получить также через нашего бота в Telegram)\n"
                                                     f"Если вы этого не делали или ID не совпали, "
                                                     f"то рекомендуем немедленно отклонить запрос "
                                                     f"и перегенерировать 'Уникальный ключ доступа' в настройках",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                    elif status == 3214:
                        vk.messages.send(user_id=source_mid,
                                         message=f"Функционал для данной социальной сети вашего профиля был приостановлен на "
                                                 f"время объединения аккаунтов социальных сетей, что НЕ может произойти в "
                                                 f"штатной ситуации. Мы уже получили оповещение об этом и вскоре свяжемся "
                                                 f"с вами для решения данной проблемы. \n"
                                                 f"Но также рекомендуем дополнительно связаться с нами по\n"
                                                 f"Email: qwerty@mail.ru",
                                         random_id=random.randint(0, 2 ** 64))
                    elif status == 15:
                        if message == 'Назад':
                            keyboard = main_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message="Выберите: ",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Как это работает?':
                            keyboard = shop_keyboard(cur_user, source_mid)
                            vk.messages.send(user_id=source_mid,
                                             message="Улучшая свои характеристики, вы облегчаете себе процесс боя. \nНапример, увеличив свою Базовую атаку, вы будете наносить больший урон своему врагу, а если защиту, то урон получаемый вами будет меньше. Аналогично со стихийными способностями, улучшая Физические характеристики, вы будете лучше атаковать или защищаться от Физического типа слаймов.",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                        elif "Лечение" in message:
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                     FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            if data[2] >= data[3]:
                                cur_user.execute(f"UPDATE Users SET Health_Points = {int(data[3])} WHERE VK_ID = {source_mid}")
                                con_user.commit()
                                keyboard = shop_keyboard(cur_user, source_mid)
                                vk.messages.send(user_id=source_mid,
                                                 message="Вы полностью здоровы",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                keyboard = shop_keyboard(cur_user, source_mid)
                                # level = exp_to_level(data[0])
                                cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
                                if cost > data[1]:
                                    vk.messages.send(user_id=source_mid,
                                                     message="Недостаточно монет",
                                                     keyboard=keyboard.get_keyboard(),
                                                     random_id=random.randint(0, 2 ** 64))
                                else:
                                    cur_user.execute(
                                        f"UPDATE Users SET Health_Points = {int(data[3])} WHERE VK_ID = {source_mid}")
                                    cur_user.execute(f"UPDATE Users SET Money = {data[1] - cost} WHERE VK_ID = {source_mid}")
                                    con_user.commit()
                                    data = cur_user.execute(
                                        f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                                                 FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                        0]
                                    vk.messages.send(user_id=source_mid,
                                                     message="Вы успешно вылечились!",
                                                     random_id=random.randint(0, 2 ** 64))
                                    keyboard = shop_keyboard(cur_user, source_mid)
                                    vk.messages.send(user_id=source_mid,
                                                     message=f"""Улучшения
                                                                Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                                Здоровье: {data[2]:,}/{data[3]:,}""",
                                                     keyboard=keyboard.get_keyboard(),
                                                     random_id=random.randint(0, 2 ** 64))
                        elif message == 'Базовые характеристики':
                            keyboard = base_shop_keyboard()
                            data = cur_user.execute(
                                f"""SELECT User_Name, Rating, Experience, 
                                                        Money, Health_Points, Max_Health_Points, 
                                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                        WHERE VK_ID = {source_mid}""").fetchall()[0]
                            k = 1.1
                            kk = 0.001
                            cost = money_coef(data[2]) * 0.2
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Характеристики
                                                        Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                        Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                        Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                        Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                        Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 105 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Дополнительные характеристики':
                            keyboard = advanced_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Категории""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 205 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        else:
                            keyboard = shop_keyboard(cur_user, source_mid)
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                     FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Улучшения
                                                         Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                         Здоровье: {data[2]:,}/{data[3]:,}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                    elif status == 105:
                        keyboard = base_shop_keyboard()
                        data = cur_user.execute(
                            f"""SELECT User_Name, Rating, Experience, 
                                        Money, Health_Points, Max_Health_Points, 
                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                        C_Attack, F_Attack, M_Attack FROM Users 
                                        WHERE VK_ID = {source_mid}""").fetchall()[0]
                        k = 1.1
                        kk = 0.001
                        cost = money_coef(data[2]) * 0.2
                        money = data[3]
                        if message == 'Базовый урон':
                            if money < max(100, int(((data[6] + 5) * k - data[6]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[6] + 5) * k - data[6]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[6] + 5) * k - data[6]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Base_Attack = {(data[6] + 5) * k} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.2
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Характеристики
                                                            Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                            Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                            Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                            Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                            Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Базовая защита':
                            if money < max(100, int(((data[7] + 5) * k - data[7]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[7] + 5) * k - data[7]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[7] + 5) * k - data[7]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Base_Shield = {(data[7] + 5) * k} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.2
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Характеристики
                                                            Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                            Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                            Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                            Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                            Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Максимальное здоровье':
                            if money < max(100, int(((data[5] + 5) * k - data[5]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[5] + 5) * k - data[5]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[5] + 5) * k - data[5]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Max_Health_Points = {int((data[5] + 5) * k)} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.2
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Характеристики
                                                            Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                            Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                            Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                            Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                            Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Критический урон':
                            if money < max(100, int(((data[8] + 15) * k - data[8]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[8] + 15) * k - data[8]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[8] + 15) * k - data[8]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Critical_Attack = {(data[8] + 1) * k} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.2
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Характеристики
                                                            Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                            Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                            Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                            Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                            Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Шанс критического урона':
                            if money < max(100, int(((data[9] + 25) * k - data[9]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                        Experience = {data[2] + max(100, int(((data[9] + 25) * k - data[9]) * cost)) * 0.05} 
                                                        WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[9] + 25) * k - data[9]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Critical_Chance = {data[9] + kk} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.2
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Характеристики
                                                            Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                            Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                            Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                            Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                            Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Назад':
                            keyboard = shop_keyboard(cur_user, source_mid)
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                     FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Улучшения
                                                                             Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                                             Здоровье: {data[2]:,}/{data[3]:,}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 15 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                        else:
                            keyboard = base_shop_keyboard()
                            data = cur_user.execute(
                                f"""SELECT User_Name, Rating, Experience, 
                                                        Money, Health_Points, Max_Health_Points, 
                                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                        WHERE VK_ID = {source_mid}""").fetchall()[0]
                            k = 1.1
                            kk = 0.001
                            cost = money_coef(data[2]) * 0.2
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Характеристики
                                                        Базовый урон: Было {data[6]:.2f} Станет: {(data[6] + 5) * k:.2f} Стоимость {max(100, int(((data[6] + 5) * k - data[6]) * cost))} монет
                                                        Базовая защита: Было {data[7]:.2f} Станет: {(data[7] + 5) * k:.2f} Стоимость {max(100, int(((data[7] + 5) * k - data[7]) * cost))} монет
                                                        Максимальное здоровье: Было {data[5]:.2f} Станет: {(data[5] + 5) * k:.2f} Стоимость {max(100, int(((data[5] + 5) * k - data[5]) * cost))} монет
                                                        Критический урон: Было {data[8]:.2f} Станет: {(data[8] + 1) * k:.2f} Стоимость {max(100, int(((data[8] + 15) * k - data[8]) * cost))} монет
                                                        Шанс критического урона: Было {data[9]:.2f} Станет: {data[9] + kk:.2f} Стоимость {max(100, int(((data[9] + 25) * k - data[9]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                    elif status == 205:
                        data = cur_user.execute(
                            f"""SELECT User_Name, Rating, Experience, 
                                        Money, Health_Points, Max_Health_Points, 
                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                        C_Attack, F_Attack, M_Attack FROM Users 
                                        WHERE VK_ID = {source_mid}""").fetchall()[0]
                        k = 1.1
                        kk = 0.001
                        cost = money_coef(data[2]) * 0.1
                        if message == 'Назад':
                            keyboard = shop_keyboard(cur_user, source_mid)
                            data = cur_user.execute(
                                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                                         FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0]
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Улучшения
                                                                                                 Ваш уровень: {exp_to_level(data[0]):,} Ваши монеты: {data[1]:,}
                                                                                                 Здоровье: {data[2]:,}/{data[3]:,}""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 15 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Физические характеристики':
                            keyboard = advanced_mini_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Физические Характеристики
                                                        Защита: Было {data[10]:.2f} Станет: {(data[10] + 10) * k:.2f} Стоимость {max(100, int(((data[10] + 10) * k - data[10]) * cost))} монет
                                                        Атака: Было {data[14]:.2f} Станет: {(data[14] + 10) * k:.2f} Стоимость {max(100, int(((data[14] + 10) * k - data[14]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 2051 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Криогенные характеристики':
                            keyboard = advanced_mini_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Криогенные характеристики
                                                        Защита: Было {data[11]:.2f} Станет: {(data[11] + 10) * k:.2f} Стоимость {max(100, int(((data[11] + 10) * k - data[11]) * cost))} монет
                                                        Атака: Было {data[15]:.2f} Станет: {(data[15] + 10) * k:.2f} Стоимость {max(100, int(((data[15] + 10) * k - data[15]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 2052 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Огненные характеристики':
                            keyboard = advanced_mini_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Огненные характеристики
                                                        Защита: Было {data[12]:.2f} Станет: {(data[12] + 10) * k:.2f} Стоимость {max(100, int(((data[12] + 10) * k - data[12]) * cost))} монет
                                                        Атака: Было {data[16]:.2f} Станет: {(data[16] + 10) * k:.2f} Стоимость {max(100, int(((data[16] + 10) * k - data[16]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 2053 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Магические характеристики':
                            keyboard = advanced_mini_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Магические характеристики
                                                        Защита: Было {data[13]:.2f} Станет: {(data[13] + 10) * k:.2f} Стоимость {max(100, int(((data[13] + 10) * k - data[13]) * cost))} монет
                                                        Атака: Было {data[17]:.2f} Станет: {(data[17] + 10) * k:.2f} Стоимость {max(100, int(((data[17] + 10) * k - data[17]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 2054 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        else:
                            keyboard = advanced_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Категории""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 205 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                    elif status in [2051, 2052, 2053, 2054]:
                        if status == 2051:
                            n_id = 10
                            v_id = 'E'
                            name = "Физические характеристики"
                        elif status == 2052:
                            n_id = 11
                            v_id = 'C'
                            name = "Криогенные характеристики"
                        elif status == 2053:
                            n_id = 12
                            v_id = 'F'
                            name = "Огненные характеристики"
                        elif status == 2054:
                            n_id = 13
                            v_id = 'M'
                            name = "Магические характеристики"
                        keyboard = advanced_mini_shop_keyboard()
                        data = cur_user.execute(
                            f"""SELECT User_Name, Rating, Experience, 
                                        Money, Health_Points, Max_Health_Points, 
                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                        C_Attack, F_Attack, M_Attack FROM Users 
                                        WHERE VK_ID = {source_mid}""").fetchall()[0]
                        k = 1.1
                        kk = 0.001
                        money = data[3]
                        cost = money_coef(data[2]) * 0.1
                        if message == 'Назад':
                            keyboard = advanced_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Категории""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            cur_user.execute(
                                f"UPDATE Users SET Status = 205 WHERE VK_ID = {source_mid}")
                            con_user.commit()
                            continue
                        elif message == 'Атака':
                            if money < max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET {v_id}_Attack = {(data[n_id + 4] + 10) * k} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.1
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                keyboard = advanced_mini_shop_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""{name}
                                                            Защита: Было {data[n_id]:.2f} Станет: {(data[n_id] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost))} монет
                                                            Атака: Было {data[n_id + 4]:.2f} Станет: {(data[n_id + 4] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        elif message == 'Защита':
                            if money < max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost)):
                                vk.messages.send(user_id=source_mid,
                                                 message="Недостаточно монет",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET 
                                                    Experience = {data[2] + max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost)) * 0.05} 
                                                    WHERE VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET 
                                Money = {money - max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost))} 
                                WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET {v_id}_Shield = {(data[n_id] + 10) * k} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                data = cur_user.execute(
                                    f"""SELECT User_Name, Rating, Experience, 
                                                                Money, Health_Points, Max_Health_Points, 
                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                WHERE VK_ID = {source_mid}""").fetchall()[0]
                                k = 1.1
                                kk = 0.001
                                cost = money_coef(data[2]) * 0.1
                                vk.messages.send(user_id=source_mid,
                                                 message="Успех!",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Монеты: {data[3]:,}",
                                                 random_id=random.randint(0, 2 ** 64))
                                keyboard = advanced_mini_shop_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""{name}
                                                            Защита: Было {data[n_id]:.2f} Станет: {(data[n_id] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost))} монет
                                                            Атака: Было {data[n_id + 4]:.2f} Станет: {(data[n_id + 4] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost))} монет""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                        else:
                            keyboard = advanced_mini_shop_keyboard()
                            vk.messages.send(user_id=source_mid,
                                             message=f"""{name}
                                                        Защита: Было {data[n_id]:.2f} Станет: {(data[n_id] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id] + 10) * k - data[n_id]) * cost))} монет
                                                        Атака: Было {data[n_id + 4]:.2f} Станет: {(data[n_id + 4] + 10) * k:.2f} Стоимость {max(100, int(((data[n_id + 4] + 10) * k - data[n_id + 4]) * cost))} монет""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            continue
                    elif status == 60:
                        type_move = None
                        if message == 'Физическая атака':
                            type_move = 'E'
                        elif message == 'Криогенная атака':
                            type_move = 'C'
                        elif message == 'Огненная атака':
                            type_move = 'F'
                        elif message == 'Магическая атака':
                            type_move = 'M'
                        if type_move is None:
                            vk.messages.send(user_id=source_mid,
                                             message=f"Вы промахнулись!",
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            cur_user.execute(f"""UPDATE Users SET Money = Money + 3 WHERE VK_ID = {source_mid}""")
                            con_user.commit()
                            vk.messages.send(user_id=source_mid,
                                             message=f"Полученные монеты за атаку: 3",
                                             random_id=random.randint(0, 2 ** 64))
                            data = cur_user.execute(
                                f"""SELECT User_Name, Rating, Experience, 
                                                                                    Money, Health_Points, Max_Health_Points, 
                                                                                    Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                                    E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                                    C_Attack, F_Attack, M_Attack FROM Users 
                                                                                    WHERE VK_ID = {source_mid}""").fetchall()[0]
                            level = exp_to_level(data[2])
                            chance = random.randint(1, 1000)
                            critical_chance = cur_user.execute(
                                f"""SELECT Critical_Chance FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0][
                                0]
                            critical_attack = cur_user.execute(
                                f"""SELECT Critical_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0][
                                0]
                            attack = cur_user.execute(
                                f"""SELECT Base_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[0][
                                0]
                            adv_attack = cur_user.execute(
                                f"""SELECT {type_move}_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                0][0]
                            if chance <= critical_chance * 1000:
                                attack = critical_attack + attack
                                adv_attack = critical_attack + attack
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Критическая атака",
                                                 random_id=random.randint(0, 2 ** 64))
                            enemy_id = cur_user.execute(
                                f"""SELECT Current_Enemy_ID FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                0][0]
                            enemy = cur_user.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                            enemy_hp = cur_user.execute(
                                f"""SELECT Current_Enemy_HP FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                0][0]
                            # print(enemy[2], type_move)
                            if enemy[2] == type_move:
                                all_damage = int((attack ** 2 + adv_attack ** 2) ** 0.5)
                                enemy_hp -= all_damage
                                cur_user.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                                con_user.commit()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Ваш удар нанес урон: {all_damage:.2f}",
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                all_damage = int(attack * 0.85)
                                enemy_hp -= all_damage
                                cur_user.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                                con_user.commit()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"Ваш удар нанес урон: {all_damage:.2f}",
                                                 random_id=random.randint(0, 2 ** 64))
                            if enemy_hp < 1:
                                enemy_exp = enemy[7]
                                enemy_money = enemy[6]
                                enemy_rating = enemy[8]
                                print(enemy_exp, enemy_money, enemy_rating)
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Вы победили!
                                                            Ваша награда
                                                            Монеты: {int(enemy_money * (level + 1) ** 1.5):,}
                                                            Опыт: {int(enemy_exp * (level + 1) ** 1.5):,}
                                                            Очки Рейтинга: {enemy_rating:,}
                                                            Здоровье: {int(data[4])}/{int(data[5])}""",
                                                 random_id=random.randint(0, 2 ** 64))
                                cur_user.execute(f"""UPDATE Users SET Experience 
                                = {data[2] + int(enemy_exp * (level + 1) ** 1.5)}, 
                                Rating = {data[1] + enemy_rating}, Money = {data[3] + int(enemy_money * (level + 1) ** 1.5)} 
                                WHERE  VK_ID = {source_mid}""")
                                cur_user.execute(f"""UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                keyboard = main_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message="Выберите: ",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                        data = cur_user.execute(
                            f"""SELECT User_Name, Rating, Experience, 
                                        Money, Health_Points, Max_Health_Points, 
                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                        C_Attack, F_Attack, M_Attack FROM Users 
                                        WHERE VK_ID = {source_mid}""").fetchall()[
                            0]
                        enemy_id = cur_user.execute(
                            f"""SELECT Current_Enemy_ID FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                            0][0]
                        enemy = cur_user.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                        enemy_hp = cur_user.execute(
                            f"""SELECT Current_Enemy_HP FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                            0][0]
                        enemy_hp_max = cur_user.execute(
                            f"""SELECT Current_Enemy_Max_HP FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                            0][0]
                        enemy_attack = cur_user.execute(
                            f"""SELECT Current_Enemy_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                            0][0]
                        vk.messages.send(user_id=source_mid,
                                         message=f"""Обнаружен враг {enemy[1]}
                                                    Здоровье: {enemy_hp}/{enemy_hp_max}
                                                    Базовый урон: {enemy_attack:.2f}""",
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=source_mid,
                                         message=f"""Враг атакует!""",
                                         random_id=random.randint(0, 2 ** 64))
                        hp = data[4]
                        chance = random.randint(1, 100)
                        keyboard = fight_keyboard()
                        if chance <= 10:
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Враг промахнулся!""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                        elif chance >= 90 and enemy_hp != enemy_hp_max:
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Враг подлечился!""",
                                             keyboard=keyboard.get_keyboard(),
                                             random_id=random.randint(0, 2 ** 64))
                            enemy_hp = min(enemy_hp_max, int(enemy_hp + enemy_hp_max * 0.1))
                            cur_user.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE VK_ID = {source_mid}""")
                            con_user.commit()
                        else:
                            shield = \
                                cur_user.execute(
                                    f"""SELECT {enemy[2]}_Shield FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                            shield_all = cur_user.execute(
                                    f"""SELECT Base_Shield FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                            hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                            vk.messages.send(user_id=source_mid,
                                             message=f"""Враг нанес вам урон: {-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f}
                                                        Ваше здоровье: {max(0, hp)}/{data[5]}""",
                                             random_id=random.randint(0, 2 ** 64))
                            if hp < 1:
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Вы проиграли""",
                                                 random_id=random.randint(0, 2 ** 64))
                                cur_user.execute(
                                    f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE VK_ID = {source_mid}""")
                                cur_user.execute(
                                    f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE VK_ID = {source_mid}""")
                                con_user.commit()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Вы потеряли
                                                            Опыт: {data[2] - int(data[2] * 0.9)}
                                                            Очки Рейтинга: {data[1] - max(0, data[1] - enemy[8] * 30)}""",
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Ваше здоровье восполнено""",
                                                 random_id=random.randint(0, 2 ** 64))
                                con_user.execute(f"""UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}""")
                                keyboard = main_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message="Выберите: ",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                cur_user.execute(
                                    f"UPDATE Users SET Status = 1 WHERE VK_ID = {source_mid}")
                                con_user.commit()
                                continue
                            else:
                                cur_user.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE VK_ID = {source_mid}""")
                                enemy_id = cur_user.execute(
                                    f"""SELECT Current_Enemy_ID FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                                enemy = cur_user.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                                enemy_hp = cur_user.execute(
                                    f"""SELECT Current_Enemy_HP FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                                enemy_hp_max = cur_user.execute(
                                    f"""SELECT Current_Enemy_Max_HP FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                                enemy_attack = cur_user.execute(
                                    f"""SELECT Current_Enemy_Attack FROM Users WHERE VK_ID = {source_mid}""").fetchall()[
                                    0][0]
                                con_user.commit()
                                keyboard = fight_keyboard()
                                vk.messages.send(user_id=source_mid,
                                                 message=f"""Обнаружен враг {enemy[1]}
                                                            Здоровье: {enemy_hp}/{enemy_hp_max}
                                                            Базовый урон: {enemy_attack:.2f}""",
                                                 keyboard=keyboard.get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
        except:
            continue


main()
