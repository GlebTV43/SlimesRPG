from aiogram import Bot, Dispatcher, types
import logging
from aiogram import Bot, types
from aiogram.utils import executor
import asyncio
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
import random
import string
import os, sys

connection = sqlite3.connect('users.db')
cur = connection.cursor()

#flags
flag = 0
#buttons
button_reg = KeyboardButton('Новый аккаунт')
button_reg1 = KeyboardButton('Подвязать')
reg_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_reg).add(button_reg1)

button_rules = KeyboardButton('Правила игры 🤯')
button_settings = KeyboardButton('Настройки ⚙️')
button_play1 = KeyboardButton('Играть 🎮')
sec_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_play1).add(button_rules).add(button_settings)

button_change_name = KeyboardButton(text='Изменить имя 👦🏼')
button_quest = KeyboardButton(text='Вопросы ❓')
button_rules = KeyboardButton('Правила игры 🤯')
button_uni_key = KeyboardButton('Уникальный ключ 🔑')
button_new_uni_key = KeyboardButton('Перегенерировать Уникальный ключ 🔑')
button_VK = KeyboardButton('Подвязать аккаунт VK')
button_back = KeyboardButton('Назад 🔙')
settings_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_change_name).add(button_quest, button_rules).add(button_uni_key, button_new_uni_key).add(button_VK).add(button_back)

button_LIKE = KeyboardButton('Принять')
button_DISLIKE = KeyboardButton('Отклонить')
VK_LIKE_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_LIKE, button_DISLIKE).add(button_back)

button_q1 = KeyboardButton(text='Что такое Очки рейтинга ❓')
button_q2 = KeyboardButton(text='Зачем нужны улучшения характеристик ❓')
questions_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_q1).add(button_q2).add(button_back)

button_menu_attack = KeyboardButton('Атаковать 💥')
button_rating = KeyboardButton('Рейтинг ⭐')
button_settings2 = KeyboardButton('Настройки 🔧')
button_fea = KeyboardButton('Стихии 🌱')
button_shop = KeyboardButton('Магазин 🛍')
button_statics = KeyboardButton('Показатели 🌈')
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_menu_attack).add(button_fea, button_rating, button_settings2).add(button_shop, button_statics)

button_E = KeyboardButton('Физические характеристики 🦾')
button_C = KeyboardButton('Криогенные характеристики 🧊')
button_F = KeyboardButton('Огненные характеристики 🔥')
button_M = KeyboardButton('Магические характеристики 🔮')
button_back = KeyboardButton('Назад 🔙')
fea_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_E).add(button_C).add(button_F).add(button_M).add(button_back)

button_shop_fea = KeyboardButton('Стихийные улучшения 🌱')
button_shop_base = KeyboardButton('Базовые улучшения 🛡')

button_base_attack = KeyboardButton('Базовый урон ⚔️')
button_base_shield = KeyboardButton('Базовая защита 🛡')
button_base_maxhp = KeyboardButton('Максимальное Здоровье ⛑')
button_base_criticaldamage = KeyboardButton('Критический урон ⚡️')
button_base_criticalchance = KeyboardButton('Шанс на Критический удар 🤞🏻')
shop_base_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_base_attack, button_base_shield).add(button_base_maxhp).add(button_base_criticaldamage, button_base_criticalchance).add(button_back)

button_attack_update = KeyboardButton('Атака ⚔️')
button_shield_update = KeyboardButton('Защита 🛡')
aors_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_attack_update).add(button_shield_update).add(button_back)

b_E_attack = KeyboardButton('Физическая Атака 🦾')
b_C_attack = KeyboardButton('Криогенная Атака 🧊')
b_F_attack = KeyboardButton('Огненная Атака 🔥')
b_M_attack = KeyboardButton('Магическая Атака 🔮')
fight_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(b_E_attack, b_C_attack).add(b_F_attack, b_M_attack)

TOKEN = '5968724782:AAESvBSx_lOPxf1Wn-reEOZj0lRabNtilr0'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


#формулы
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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


#цена лечения
#data = cur.execute(
        #f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                 #FROM Users WHERE VK_ID = {user_id}""").fetchall()[0]
#cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
#if data[3] / data[2] == 1:
    #cost = 0


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if not cur.execute(f'SELECT * FROM Users WHERE TG_ID = {user_id}').fetchall():
        username = message.from_user.first_name
        await message.reply(f'Здравствуйте {username}, вы попали игру чат-бот Slimes RPG. \n'
                            f'Если хотите продолжить, то вам необходимо зарегистрироваться!', reply_markup=reg_kb)
    else:
        username = message.from_user.first_name
        await message.reply(f'{username}, вы уже зарегестрированы! 😡')


@dp.message_handler(content_types=['text'])
async def bot_mes(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.first_name
    if message.chat.type == 'private':
        if not cur.execute(f"SELECT Status FROM Users WHERE TG_ID = {user_id}").fetchall():
            # print(cur.execute(f"SELECT Status FROM Users WHERE TG_ID = {user_id}").fetchall()[0][0])
            cur.execute(
                f"INSERT INTO Users (User_Name, Status, TG_ID) VALUES ('{username}', -2, {user_id})")
            connection.commit()
        if message.text == 'Новый аккаунт':
            user_id = message.from_user.id
            username = message.from_user.first_name
            # cur.execute(f"INSERT INTO Users (User_Name, TG_ID, status) VALUES ('{username}', {user_id}, {1})")
            while True:
                lenth = 100
                tmp = cur.execute(f"SELECT User_ID FROM Users WHERE TG_ID = {user_id}").fetchall()[0][
                    0]
                unique_id = str(user_id) + str(tmp) + id_generator(lenth - len(str(user_id) + str(tmp)))
                if cur.execute(f"SELECT * FROM Users WHERE Unique_ID = '{unique_id}'").fetchall():
                    continue
                cur.execute(f"UPDATE Users SET Unique_ID = '{unique_id}' WHERE TG_ID = {user_id}")
                connection.commit()
                break
            cur.execute(f"UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}")
            cur.execute(f"UPDATE Users SET Unique_ID = '{unique_id}' WHERE TG_ID = {user_id}")
            connection.commit()
            await bot.send_message(message.chat.id, 'Вы успешно зарегистрировались!', reply_markup=sec_kb)
        elif message.text == 'Подвязать':
            await bot.send_message(message.chat.id,
                                     f"Ваш ID в TG: {user_id}")
            if not cur.execute(f'SELECT * FROM Users WHERE TG_ID = {user_id}').fetchall():
                cur.execute(
                    f"INSERT INTO Users (Status, TG_ID) VALUES (-2, {user_id})")
            connection.commit()
            await bot.send_message(message.chat.id,
                                   f"Введите ваш Уникальный ключ доступа:")
        elif cur.execute(f"SELECT Status FROM Users WHERE TG_ID = {user_id}").fetchall()[0][0] == -2:
            cur.execute(f"UPDATE Users SET TG_ID_REG = {user_id} WHERE Unique_ID = '{message.text}'")
            connection.commit()
            await bot.send_message(message.chat.id, "Вам необходимо подтвердить привязку из аккаунта VK")
            cur.execute(f"UPDATE Users SET Status = -2 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Правила игры 🤯':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {11} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, f'*Правила игры:*\n'
f'_Вас атакуют монстры, единственное, что вы можете сделать, это смириться и приспособиться к этому, улучшая свои характеристики. За каждого выигрыного слайма вы получаете рейтинг. Соревнуйтесь с друзьями, проверяя свой рейтинг на сайте игры._', parse_mode='Markdown')
        elif message.text == 'Настройки ⚙️':
            user_id = message.from_user.id
            print('Настройки')
            cur.execute(f'''UPDATE Users SET status = {14} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, 'Настройки.',
                                   reply_markup=settings_kb)
        elif message.text == 'Настройки 🔧':
            user_id = message.from_user.id
            print('Настройки2')
            cur.execute(f'''UPDATE Users SET status = {14} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, 'Настройки',
                                   reply_markup=settings_kb)
        elif message.text == 'Подвязать аккаунт VK':
            vk_id_reg = cur.execute(f"SELECT VK_ID_REG FROM Users WHERE "
                                         f"TG_ID = {user_id}").fetchall()[0][0]
            if vk_id_reg is not None:
                await bot.send_message(message.chat.id,
                f"Аккаунт VK с ID {vk_id_reg} хочет подвязаться к вашему "
                                         f"профилю.\n"
                                         f"Сравните данный ID с ID вашего аккаунта Telegram. "
                                         f"(Его вы можете получить также через нашего бота в Telegram)\n"
                                         f"Если вы этого не делали или ID не совпали, "
                                         f"то рекомендуем немедленно отклонить запрос "
                                         f"и перегенерировать 'Уникальный ключ доступа' в настройках", reply_markup=VK_LIKE_kb)
                cur.execute(
                    f"UPDATE Users SET Status = 3114 WHERE TG_ID = {user_id}")
                connection.commit()
            else:
                await bot.send_message(message.chat.id, f"Не обнаружено входящих запросов")
        elif message.text == 'Принять':
            vk_id_reg = cur.execute(f"SELECT VK_ID_REG FROM Users WHERE "
                                    f"TG_ID = {user_id}").fetchall()[0][0]
            cur.execute(f"DELETE FROM Users WHERE VK_ID = '{vk_id_reg}'")
            cur.execute(
                f"UPDATE Users SET VK_ID = '{vk_id_reg}' WHERE TG_ID = {user_id}")
            cur.execute(
                f"UPDATE Users SET VK_ID_REG = NULL WHERE TG_ID = {user_id}")
            cur.execute(
                f"UPDATE Users SET Status = 14 WHERE TG_ID = {user_id}")
            connection.commit()
            await bot.send_message(message.chat.id, f"Telegram аккаунт с ID {user_id} и VK аккаунт с ID {vk_id_reg} "
                                     f"теперь объединены", reply_markup=settings_kb)
        elif message == 'Отклонить':
            cur.execute(
                f"UPDATE Users SET VK_ID_REG = NULL WHERE TG_ID = {user_id}")
            cur.execute(
                f"UPDATE Users SET Status = 14 WHERE TG_ID = {user_id}")
            connection.commit()
            await bot.send_message(message.chat.id, f"Запрос на добавление Telegram аккаунта был отклонен", reply_markup=settings_kb)
        elif message.text == 'Вопросы ❓':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {141} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, 'Вопросы',
                                   reply_markup=questions_kb)
        elif message.text == 'Что такое Очки рейтинга ❓':
            user_id = message.from_user.id
            await bot.send_message(message.chat.id, f'*Что такое Очки рейтинга ❓*\n'
                                   f'_С помощью Очков рейтинга, получаемого при победе в бою, вы повышаете свое место в общем рейтинге игроков.\nОбщий рейтинг: http://185.185.71.200:8080_', parse_mode='Markdown')
        elif message.text == 'Зачем нужны улучшения характеристик ❓':
            user_id = message.from_user.id
            await bot.send_message(message.chat.id, f'*Зачем нужны улучшения характеристик ❓*\n'
                                                    f'_Улучшая свои характеристики, вы облегчаете себе процесс боя. Например, увеличив свою Базовую атаку, вы будете наносить больший урон своему врагу, а если защиту, то урон получаемый вами будет меньше. Аналогично со стихийными способностями, улучшая Физические характеристики, вы будете лучше атаковать или защищаться от Физического типа слаймов._',
                                   parse_mode='Markdown')
        elif message.text == 'Уникальный ключ 🔑':
            code = cur.execute(f"SELECT Unique_ID FROM Users WHERE TG_ID = {user_id}").fetchall()[0][
                0]
            await bot.send_message(message.chat.id, f'*Ваш уникальный ключ доступа:*\n'
                                                    f'{code}', parse_mode='Markdown')
        elif message.text == 'Перегенерировать Уникальный ключ 🔑':
            while True:
                lenth = 100
                tmp = cur.execute(f"SELECT User_ID FROM Users WHERE TG_ID = {user_id}").fetchall()[0][
                    0]
                unique_id = str(user_id) + str(tmp) + id_generator(lenth - len(str(user_id) + str(tmp)))
                if cur.execute(f"SELECT * FROM Users WHERE Unique_ID = '{unique_id}'").fetchall():
                    continue
                cur.execute(f"UPDATE Users SET Unique_ID = '{unique_id}' WHERE TG_ID = {user_id}")
                connection.commit()
                break
            await bot.send_message(message.chat.id, f'*Ваш новый уникальный ключ доступа:*\n'
                                                    f'{unique_id}', parse_mode='Markdown')
        elif message.text == 'Подвязать аккаунт VK':
            code = cur.execute(f"SELECT Unique_ID FROM Users WHERE TG_ID = {user_id}").fetchall()[0][
                0]
            await bot.send_message(message.chat.id, f'Ваш уникальный ключ доступа:\n'
                                                    f'{code}', parse_mode='Markdown')
        elif message.text == 'Изменить имя 👦🏼':
            user_id = message.from_user.id
            print('Изменить имя')
            cur.execute(f'''UPDATE Users SET status = {214} WHERE TG_ID = {user_id}''')
            connection.commit()
            username = message.from_user.first_name
            await bot.send_message(message.chat.id, f'Введите новое имя.\n'
                                                    f'Старое имя: {username}')
            await bot.send_message(message.chat.id, f'Введите в формате "$$#имя#"')
        elif message.text.startswith('$$'):
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET User_Name = '{message.text.strip('$$')}' WHERE TG_ID = {user_id}''')
            connection.commit()
            print(f'имя изменено на {message.text.strip("$$")}')
            nn = cur.execute(f'''SELECT User_Name FROM Users WHERE TG_ID = {user_id}''').fetchall()[0]
            connection.commit()
            await bot.send_message(message.chat.id, f'Отлично! \n'
                                                    f'Теперь вы: {nn[0]}')

        elif message.text == 'Назад 🔙':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            print(status)
            if status == 11:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            if status == 14:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            if status == 141:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=settings_kb)
                cur.execute(f'''UPDATE Users SET status = {14} WHERE TG_ID = {user_id}''')
                connection.commit()
            elif status == 214:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            elif status == 1:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            elif status == 12:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            elif status == 15:
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=menu_kb)
                cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
                connection.commit()
            elif status in [105, 205]:
                cur.execute(f'''UPDATE Users SET status = {15} WHERE TG_ID = {user_id}''')
                connection.commit()
                money = cur.execute(f'''SELECT Money FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
                user_id = message.from_user.id
                data = cur.execute(
                    f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                         FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
                if data[3] / data[2] == 1:
                    cost = 0
                button_heal = KeyboardButton(f'Лечение ⛑ ({cost} 💸)')
                shop_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_shop_fea, button_shop_base).add(
                    button_heal).add(button_back)
                await bot.send_message(message.chat.id, 'Вы вернулись.', reply_markup=shop_kb)
            elif status in [2051, 2052, 2053, 2054]:
                await bot.send_message(message.chat.id, 'Вы вернулись.\n'
                                                        'Выберете, что хотите улучшить:', reply_markup=fea_kb)
                cur.execute(f'''UPDATE Users SET status = {205} WHERE TG_ID = {user_id}''')
                connection.commit()
        elif message.text == 'Играть 🎮':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {1} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, 'Вы в игре! 🕹', reply_markup=menu_kb)
        elif message.text == 'Атаковать 💥':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {60} WHERE TG_ID = {user_id}''')
            connection.commit()
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                Money, Health_Points, Max_Health_Points, 
                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                WHERE TG_ID = {user_id}""").fetchall()[0]
            level = exp_to_level(data[2])
            base = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_Level <= {level}""").fetchall()
            enemy = random.choice(base)
            cur.execute(f"""UPDATE Users SET Current_Enemy_ID = {enemy[0]} WHERE TG_ID = {user_id}""")
            cur.execute(
                f"""UPDATE Users SET Current_Enemy_HP = {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} WHERE TG_ID = {user_id}""")
            cur.execute(
                f"""UPDATE Users SET Current_Enemy_Max_HP = {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} WHERE TG_ID = {user_id}""")
            cur.execute(
                f"""UPDATE Users SET Current_Enemy_Attack = {max(enemy[4], enemy[4] * 0.01 ** (0.5 * level))} WHERE TG_ID = {user_id}""")
            connection.commit()
            await bot.send_message(message.chat.id, f'Обнаружен враг: {enemy[1]}\n'
                                                f'_Здоровье_: {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} ❤️/ {max(enemy[3], int(enemy[3] * 0.01 ** (0.5 * level)))} ❤️\n'
                                                f'_Базовый урон_: {max(enemy[4], enemy[4] * 0.01 ** (0.5 * level)):.2f} ⚔️', reply_markup=fight_kb, parse_mode='Markdown')
        elif message.text == 'Физическая Атака 🦾':
            cur.execute(f"""UPDATE Users SET Money = Money + 3 WHERE TG_ID = {user_id}""")
            connection.commit()
            await bot.send_message(message.chat.id, f'Вы получили 3 монеты 💸')
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                                                        Money, Health_Points, Max_Health_Points, 
                                                                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                                                        WHERE TG_ID = {user_id}""").fetchall()[
                0]
            level = exp_to_level(data[2])
            chance = random.randint(1, 1000)
            critical_chance = cur.execute(
                f"""SELECT Critical_Chance FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            critical_attack = cur.execute(
                f"""SELECT Critical_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            attack = cur.execute(
                f"""SELECT Base_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            adv_attack = cur.execute(
                f"""SELECT E_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if chance <= critical_chance * 1000:
                attack = critical_attack + attack
                adv_attack = critical_attack + attack
                await bot.send_message(message.chat.id, f'Критическая Атака ⚡️')
            enemy_id = cur.execute(
                f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
            enemy_hp = cur.execute(
                f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if enemy[2] == 'E':
                all_damage = int((attack ** 2 + adv_attack ** 2) ** 0.5)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            else:
                all_damage = int(attack * 0.85)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            if enemy_hp < 1:
                enemy_exp = enemy[7]
                enemy_money = enemy[6]
                enemy_rating = enemy[8]
                print(enemy_exp, enemy_money, enemy_rating)
                await bot.send_message(message.chat.id,
                                       f"*Вы победили!*\n\n*Ваша награда*:\n"
                                       f"_Монеты_: *{int(enemy_money * (level + 1) ** 1.5):,} 💸*\n"
                                       f"_Опыт_: *{int(enemy_exp * (level + 1) ** 1.5):,} ⭐️*\n"
                                       f"_Очки Рейтинга_: *{enemy_rating:,} 🏆*\n"
                                       f"_Здоровье_: *{int(data[4])} ❤/ {int(data[5])} ❤ ️*", reply_markup=menu_kb,
                                       parse_mode='Markdown')
                cur.execute(f"""UPDATE Users SET Experience 
                = {data[2] + int(enemy_exp * (level + 1) ** 1.5)}, 
                Rating = {data[1] + enemy_rating}, Money = {data[3] + int(enemy_money * (level + 1) ** 1.5)} 
                WHERE  TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                connection.commit()
            else:
                data = cur.execute(
                    f"""SELECT User_Name, Rating, Experience, 
                                                Money, Health_Points, Max_Health_Points, 
                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                enemy_id = cur.execute(
                    f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                enemy_hp = cur.execute(
                    f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_hp_max = cur.execute(
                    f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_attack = cur.execute(
                    f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                await bot.send_message(message.chat.id, f'ВАС АТАКУЕТ *{enemy[1]}*\n\n'
                                                        f'_Здоровье_: *{enemy_hp} ❤️/ {enemy_hp_max} ❤️*\n'
                                                        f'_Базовый урон_: *{enemy_attack:.2f}*\n',
                                       parse_mode='Markdown')
                hp = data[4]
                chance = random.randint(1, 100)
                if chance <= 10:
                    await bot.send_message(message.chat.id, f'ФУХ, враг *промахнулся*', parse_mode='Markdown')
                elif chance >= 90 and enemy_hp != enemy_hp_max:
                    await bot.send_message(message.chat.id, f'Враг *подлечился* ⛑', parse_mode='Markdown')
                    cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE TG_ID = {user_id}""")
                    connection.commit()
                else:
                    shield = \
                        cur.execute(
                            f"""SELECT {enemy[2]}_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                    shield_all = cur.execute(
                        f"""SELECT Base_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                    await bot.send_message(message.chat.id,
                                           f'_Враг нанес вам урон_: *{-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f} ❤*\n'
                                           f'_Ваше здоровье_: *{max(0, hp)} ❤️/ {data[5]} ❤️*', parse_mode='Markdown')
                    if hp < 1:
                        cur.execute(
                            f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE TG_ID = {user_id}""")
                        connection.commit()
                        await bot.send_message(message.chat.id, f'*Вы проиграли* ☠️\n\n'
                                                                f'Вы потеряли:\n'
                                                                f'_Опыт_: *{data[2] - int(data[2] * 0.9)}* ⭐️\n'
                                                                f'_Очки Рейтинга_: *{data[1] - max(0, data[1] - enemy[8] * 30)}* 🏆\n'
                                                                f'\n'
                                                                f'_Ваше здоровье восполненно_', reply_markup=menu_kb,
                                               parse_mode='Markdown')

                        cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                        connection.commit()
                    else:
                        cur.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE TG_ID = {user_id}""")
                        enemy_id = cur.execute(
                            f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                        enemy_hp = cur.execute(
                            f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_hp_max = cur.execute(
                            f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_attack = cur.execute(
                            f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        connection.commit()
                        #вас атакует
        elif message.text == 'Криогенная Атака 🧊':
            cur.execute(f"""UPDATE Users SET Money = Money + 3 WHERE TG_ID = {user_id}""")
            connection.commit()
            await bot.send_message(message.chat.id, f'Вы получили 3 монеты 💸')
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                                                                    Money, Health_Points, Max_Health_Points, 
                                                                                                    Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                                                    E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                                                    C_Attack, F_Attack, M_Attack FROM Users 
                                                                                                    WHERE TG_ID = {user_id}""").fetchall()[
                0]
            level = exp_to_level(data[2])
            chance = random.randint(1, 1000)
            critical_chance = cur.execute(
                f"""SELECT Critical_Chance FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            critical_attack = cur.execute(
                f"""SELECT Critical_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            attack = cur.execute(
                f"""SELECT Base_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            adv_attack = cur.execute(
                f"""SELECT C_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if chance <= critical_chance * 1000:
                attack = critical_attack + attack
                adv_attack = critical_attack + attack
                await bot.send_message(message.chat.id, f'Критическая Атака ⚡️')
            enemy_id = cur.execute(
                f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
            enemy_hp = cur.execute(
                f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if enemy[2] == 'C':
                all_damage = int((attack ** 2 + adv_attack ** 2) ** 0.5)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            else:
                all_damage = int(attack * 0.85)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            if enemy_hp < 1:
                enemy_exp = enemy[7]
                enemy_money = enemy[6]
                enemy_rating = enemy[8]
                print(enemy_exp, enemy_money, enemy_rating)
                await bot.send_message(message.chat.id,
                                       f"*Вы победили!*\n\n*Ваша награда*:\n"
                                       f"_Монеты_: *{int(enemy_money * (level + 1) ** 1.5):,} 💸*\n"
                                       f"_Опыт_: *{int(enemy_exp * (level + 1) ** 1.5):,} ⭐️*\n"
                                       f"_Очки Рейтинга_: *{enemy_rating:,} 🏆*\n"
                                       f"_Здоровье_: *{int(data[4])} ❤/ {int(data[5])} ❤ ️*", reply_markup=menu_kb,
                                       parse_mode='Markdown')
                cur.execute(f"""UPDATE Users SET Experience 
                            = {data[2] + int(enemy_exp * (level + 1) ** 1.5)}, 
                            Rating = {data[1] + enemy_rating}, Money = {data[3] + int(enemy_money * (level + 1) ** 1.5)} 
                            WHERE  TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                connection.commit()
            else:
                data = cur.execute(
                    f"""SELECT User_Name, Rating, Experience, 
                                                            Money, Health_Points, Max_Health_Points, 
                                                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                            E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                            C_Attack, F_Attack, M_Attack FROM Users 
                                                            WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                enemy_id = cur.execute(
                    f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                enemy_hp = cur.execute(
                    f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_hp_max = cur.execute(
                    f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_attack = cur.execute(
                    f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                await bot.send_message(message.chat.id, f'ВАС АТАКУЕТ *{enemy[1]}*\n\n'
                                                        f'_Здоровье_: *{enemy_hp} ❤️/ {enemy_hp_max} ❤️*\n'
                                                        f'_Базовый урон_: *{enemy_attack:.2f}*\n',
                                       parse_mode='Markdown')
                hp = data[4]
                chance = random.randint(1, 100)
                if chance <= 10:
                    await bot.send_message(message.chat.id, f'ФУХ, враг *промахнулся*', parse_mode='Markdown')
                elif chance >= 90 and enemy_hp != enemy_hp_max:
                    await bot.send_message(message.chat.id, f'Враг *подлечился* ⛑', parse_mode='Markdown')
                    cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE TG_ID = {user_id}""")
                    connection.commit()
                else:
                    shield = \
                        cur.execute(
                            f"""SELECT {enemy[2]}_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                    shield_all = cur.execute(
                        f"""SELECT Base_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                    await bot.send_message(message.chat.id,
                                           f'_Враг нанес вам урон_: *{-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f} ❤*\n'
                                           f'_Ваше здоровье_: *{max(0, hp)} ❤️/ {data[5]} ❤️*', parse_mode='Markdown')
                    if hp < 1:
                        cur.execute(
                            f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE TG_ID = {user_id}""")
                        connection.commit()
                        await bot.send_message(message.chat.id, f'*Вы проиграли* ☠️\n\n'
                                                                f'Вы потеряли:\n'
                                                                f'_Опыт_: *{data[2] - int(data[2] * 0.9)}* ⭐️\n'
                                                                f'_Очки Рейтинга_: *{data[1] - max(0, data[1] - enemy[8] * 30)}* 🏆\n'
                                                                f'\n'
                                                                f'_Ваше здоровье восполненно_', reply_markup=menu_kb,
                                               parse_mode='Markdown')
                        cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                        connection.commit()
                    else:
                        cur.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE TG_ID = {user_id}""")
                        enemy_id = cur.execute(
                            f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                        enemy_hp = cur.execute(
                            f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_hp_max = cur.execute(
                            f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_attack = cur.execute(
                            f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        connection.commit()
                        #вас атакует
        elif message.text == 'Огненная Атака 🔥':
            cur.execute(f"""UPDATE Users SET Money = Money + 3 WHERE TG_ID = {user_id}""")
            connection.commit()
            await bot.send_message(message.chat.id, f'Вы получили 3 монеты 💸')
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                                                                                Money, Health_Points, Max_Health_Points, 
                                                                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                                                                WHERE TG_ID = {user_id}""").fetchall()[
                0]
            level = exp_to_level(data[2])
            chance = random.randint(1, 1000)
            critical_chance = cur.execute(
                f"""SELECT Critical_Chance FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            critical_attack = cur.execute(
                f"""SELECT Critical_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            attack = cur.execute(
                f"""SELECT Base_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            adv_attack = cur.execute(
                f"""SELECT F_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if chance <= critical_chance * 1000:
                attack = critical_attack + attack
                adv_attack = critical_attack + attack
                await bot.send_message(message.chat.id, f'Критическая Атака ⚡️')
            enemy_id = cur.execute(
                f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
            enemy_hp = cur.execute(
                f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if enemy[2] == 'F':
                all_damage = int((attack ** 2 + adv_attack ** 2) ** 0.5)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            else:
                all_damage = int(attack * 0.85)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            if enemy_hp < 1:
                enemy_exp = enemy[7]
                enemy_money = enemy[6]
                enemy_rating = enemy[8]
                print(enemy_exp, enemy_money, enemy_rating)
                await bot.send_message(message.chat.id,
                                       f"*Вы победили!*\n\n*Ваша награда*:\n"
                                       f"_Монеты_: *{int(enemy_money * (level + 1) ** 1.5):,} 💸*\n"
                                       f"_Опыт_: *{int(enemy_exp * (level + 1) ** 1.5):,} ⭐️*\n"
                                       f"_Очки Рейтинга_: *{enemy_rating:,} 🏆*\n"
                                       f"_Здоровье_: *{int(data[4])} ❤/ {int(data[5])} ❤ ️*", reply_markup=menu_kb,
                                       parse_mode='Markdown')
                cur.execute(f"""UPDATE Users SET Experience 
                                        = {data[2] + int(enemy_exp * (level + 1) ** 1.5)}, 
                                        Rating = {data[1] + enemy_rating}, Money = {data[3] + int(enemy_money * (level + 1) ** 1.5)} 
                                        WHERE  TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                connection.commit()
            else:
                data = cur.execute(
                    f"""SELECT User_Name, Rating, Experience, 
                                                                        Money, Health_Points, Max_Health_Points, 
                                                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                                        WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                enemy_id = cur.execute(
                    f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                enemy_hp = cur.execute(
                    f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_hp_max = cur.execute(
                    f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_attack = cur.execute(
                    f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                await bot.send_message(message.chat.id, f'ВАС АТАКУЕТ *{enemy[1]}*\n\n'
                                                        f'_Здоровье_: *{enemy_hp} ❤️/ {enemy_hp_max} ❤️*\n'
                                                        f'_Базовый урон_: *{enemy_attack:.2f}*\n',
                                       parse_mode='Markdown')
                hp = data[4]
                chance = random.randint(1, 100)
                if chance <= 10:
                    await bot.send_message(message.chat.id, f'ФУХ, враг *промахнулся*', parse_mode='Markdown')
                elif chance >= 90 and enemy_hp != enemy_hp_max:
                    await bot.send_message(message.chat.id, f'Враг *подлечился* ⛑', parse_mode='Markdown')
                    cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE TG_ID = {user_id}""")
                    connection.commit()
                else:
                    shield = \
                        cur.execute(
                            f"""SELECT {enemy[2]}_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                    shield_all = cur.execute(
                        f"""SELECT Base_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                    await bot.send_message(message.chat.id,
                                           f'_Враг нанес вам урон_: *{-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f} ❤*\n'
                                           f'_Ваше здоровье_: *{max(0, hp)} ❤️/ {data[5]} ❤️*', parse_mode='Markdown')
                    if hp < 1:
                        cur.execute(
                            f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE TG_ID = {user_id}""")
                        connection.commit()
                        await bot.send_message(message.chat.id, f'*Вы проиграли* ☠️\n\n'
                                                                f'Вы потеряли:\n'
                                                                f'_Опыт_: *{data[2] - int(data[2] * 0.9)}* ⭐️\n'
                                                                f'_Очки Рейтинга_: *{data[1] - max(0, data[1] - enemy[8] * 30)}* 🏆\n'
                                                                f'\n'
                                                                f'_Ваше здоровье восполненно_', reply_markup=menu_kb,
                                               parse_mode='Markdown')
                        cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                        connection.commit()
                    else:
                        cur.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE TG_ID = {user_id}""")
                        enemy_id = cur.execute(
                            f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                        enemy_hp = cur.execute(
                            f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_hp_max = cur.execute(
                            f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_attack = cur.execute(
                            f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        connection.commit()
                        #вас атакует
        elif message.text == 'Магическая Атака 🔮':
            cur.execute(f"""UPDATE Users SET Money = Money + 3 WHERE TG_ID = {user_id}""")
            connection.commit()
            await bot.send_message(message.chat.id, f'Вы получили 3 монеты 💸')
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                                                                                Money, Health_Points, Max_Health_Points, 
                                                                                                                Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                                                                E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                                                                C_Attack, F_Attack, M_Attack FROM Users 
                                                                                                                WHERE TG_ID = {user_id}""").fetchall()[
                0]
            level = exp_to_level(data[2])
            chance = random.randint(1, 1000)
            critical_chance = cur.execute(
                f"""SELECT Critical_Chance FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            critical_attack = cur.execute(
                f"""SELECT Critical_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            attack = cur.execute(
                f"""SELECT Base_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[0][
                0]
            adv_attack = cur.execute(
                f"""SELECT M_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if chance <= critical_chance * 1000:
                attack = critical_attack + attack
                adv_attack = critical_attack + attack
                await bot.send_message(message.chat.id, f'Критическая Атака ⚡️')
            enemy_id = cur.execute(
                f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
            enemy_hp = cur.execute(
                f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            if enemy[2] == 'M':
                all_damage = int((attack ** 2 + adv_attack ** 2) ** 0.5)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            else:
                all_damage = int(attack * 0.85)
                enemy_hp -= all_damage
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp}""")
                connection.commit()
                await bot.send_message(message.chat.id, f'_Ваша атака нанесла_: *{all_damage:.2f} ❤️*️', parse_mode='Markdown')
            if enemy_hp < 1:
                enemy_exp = enemy[7]
                enemy_money = enemy[6]
                enemy_rating = enemy[8]
                print(enemy_exp, enemy_money, enemy_rating)
                await bot.send_message(message.chat.id,
                                       f"*Вы победили!*\n\n*Ваша награда*:\n"
                                       f"_Монеты_: *{int(enemy_money * (level + 1) ** 1.5):,} 💸*\n"
                                       f"_Опыт_: *{int(enemy_exp * (level + 1) ** 1.5):,} ⭐️*\n"
                                       f"_Очки Рейтинга_: *{enemy_rating:,} 🏆*\n"
                                       f"_Здоровье_: *{int(data[4])} ❤/ {int(data[5])} ❤ ️*", reply_markup=menu_kb, parse_mode='Markdown')
                cur.execute(f"""UPDATE Users SET Experience 
                                        = {data[2] + int(enemy_exp * (level + 1) ** 1.5)}, 
                                        Rating = {data[1] + enemy_rating}, Money = {data[3] + int(enemy_money * (level + 1) ** 1.5)} 
                                        WHERE  TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                connection.commit()
            else:
                data = cur.execute(
                    f"""SELECT User_Name, Rating, Experience, 
                                                                        Money, Health_Points, Max_Health_Points, 
                                                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                                        E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                                        WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                enemy_id = cur.execute(
                    f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                enemy_hp = cur.execute(
                    f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_hp_max = cur.execute(
                    f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                enemy_attack = cur.execute(
                    f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                await bot.send_message(message.chat.id, f'ВАС АТАКУЕТ *{enemy[1]}*\n\n'
                                                        f'_Здоровье_: *{enemy_hp} ❤️/ {enemy_hp_max} ❤️*\n'
                                                        f'_Базовый урон_: *{enemy_attack:.2f}*\n',
                                       parse_mode='Markdown')
                hp = data[4]
                chance = random.randint(1, 100)
                if chance <= 10:
                    await bot.send_message(message.chat.id, f'ФУХ, враг *промахнулся*', parse_mode='Markdown')
                elif chance >= 90 and enemy_hp != enemy_hp_max:
                    await bot.send_message(message.chat.id, f'Враг *подлечился* ⛑', parse_mode='Markdown')
                    cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE TG_ID = {user_id}""")
                    connection.commit()
                else:
                    shield = \
                        cur.execute(
                            f"""SELECT {enemy[2]}_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                    shield_all = cur.execute(
                        f"""SELECT Base_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                    await bot.send_message(message.chat.id,
                                           f'_Враг нанес вам урон_: *{-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f} ❤*\n'
                                           f'_Ваше здоровье_: *{max(0, hp)} ❤️/ {data[5]} ❤️*', parse_mode='Markdown')
                    if hp < 1:
                        cur.execute(
                            f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE TG_ID = {user_id}""")
                        cur.execute(
                            f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE TG_ID = {user_id}""")
                        connection.commit()
                        await bot.send_message(message.chat.id, f'*Вы проиграли* ☠️\n\n'
                                                                f'Вы потеряли:\n'
                                                                f'_Опыт_: *{data[2] - int(data[2] * 0.9)}* ⭐️\n'
                                                                f'_Очки Рейтинга_: *{data[1] - max(0, data[1] - enemy[8] * 30)}* 🏆\n'
                                                                f'\n'
                                                                f'_Ваше здоровье восполненно_', reply_markup=menu_kb,
                                               parse_mode='Markdown')
                        cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                        connection.commit()
                    else:
                        cur.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE TG_ID = {user_id}""")
                        enemy_id = cur.execute(
                            f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                        enemy_hp = cur.execute(
                            f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_hp_max = cur.execute(
                            f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        enemy_attack = cur.execute(
                            f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                            0][0]
                        connection.commit()
                        #вас атакует
        elif message.text == 'Рейтинг ⭐':
            cur.execute(f'''UPDATE Users SET status = {13} WHERE TG_ID = {user_id}''')
            connection.commit()
            all_rating = cur.execute(f"SELECT VK_ID, TG_ID, Rating FROM Users").fetchall()
            all_rating.sort(key=lambda x: x[2], reverse=True)
            current_row = cur.execute(
                f"SELECT VK_ID, TG_ID, Rating FROM Users WHERE TG_ID = {user_id}").fetchall()
            rating = all_rating.index(current_row[0])
            user_id = message.from_user.id
            raiting = cur.execute(f'''SELECT Rating FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            connection.commit()
            await bot.send_message(message.chat.id, f'_Ваш рейтинг_: *{rating + 1}* 🏆\n'
                                                    f'_Ваши очки_: *{raiting}*  ⭐\n'
                                                    f'_Общий рейтинг: http://185.185.71.200:8080_', reply_markup=menu_kb, parse_mode='Markdown')
        elif message.text == 'Стихии 🌱':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {12} WHERE TG_ID = {user_id}''')
            connection.commit()
            await bot.send_message(message.chat.id, 'Тут вы можете смотреть на ваши стихийные характеристики.',
                                   reply_markup=fea_kb)
        elif message.text == 'Магазин 🛍':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {15} WHERE TG_ID = {user_id}''')
            money = cur.execute(f'''SELECT Money FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(
                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                                                 FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
            if data[3] / data[2] == 1:
                cost = 0
            connection.commit()
            button_heal = KeyboardButton(f'Лечение ⛑ ({cost} 💸)')
            shop_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_shop_fea, button_shop_base).add(
                button_heal).add(button_back)
            await bot.send_message(message.chat.id, 'Тут вы можете улучшать ваши характеристики. \n'
                                                    f'_Количество монет_: *{money}* 💸',
                                   reply_markup=shop_kb, parse_mode='Markdown')
        elif 'Лечение' in message.text:
            user_id = message.from_user.id
            data = cur.execute(
                f"""SELECT Experience, Money, Health_Points, Max_Health_Points
                                                                     FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            cost = int(money_coef(data[0]) * 0.03 * min(4, (data[3] / data[2])))
            if data[3] / data[2] == 1:
                cost = 0
            button_heal = KeyboardButton(f'Лечение ⛑ ({cost} 💸)')
            shop_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_shop_fea, button_shop_base).add(
                button_heal).add(button_back)
            if data[2] >= data[3]:
                cur.execute(f"UPDATE Users SET Health_Points = {int(data[3])} WHERE TG_ID = {user_id}")
                connection.commit()
                await bot.send_message(message.chat.id, "_Вы полностью здоровы_",
                                       reply_markup=shop_kb, parse_mode='Markdown')
            else:
                if cost > data[1]:
                    await bot.send_message(message.chat.id, "Недостаточно монет(",
                                           reply_markup=shop_kb)
                else:
                    cur.execute(
                        f"UPDATE Users SET Health_Points = {int(data[3])} WHERE TG_ID = {user_id}")
                    cur.execute(f"UPDATE Users SET Money = {data[1] - cost} WHERE TG_ID = {user_id}")
                    connection.commit()
                    await bot.send_message(message.chat.id, "_Вы полностью здоровы_",
                                           reply_markup=shop_kb, parse_mode='Markdown')
        elif message.text == 'Базовые улучшения 🛡':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[2]) * 0.2
            await bot.send_message(message.chat.id, f'Базовый урон: \nБыло: {data[1]:.2f} ⚔️ \nСтанет: {(data[1] + 5) * k:.2f} ⚔️\nСтоимость: {max(100, int(((data[1] + 5) * k - data[1]) * cost))} 💸 '
                                                    f'\nБазовая защита: \nБыло: {data[2]:.2f} 🛡 \nСтанет: {(data[2] + 5) * k:.2f} 🛡 \nСтоимость: {max(100, int(((data[2] + 5) * k - data[2]) * cost))} 💸 '
                                                    f'\nМаксимальное здоровье:\nБыло: {data[0]:.2f} ⛑ \nСтанет: {(data[0] + 5) * k:.2f} ⛑ \nСтоимость: {max(100, int(((data[0] + 5) * k - data[0]) * cost))} 💸 '
                                                    f'\nКритический урон: \nБыло: {data[3]:.2f}  ⚡️ \nСтанет: {(data[3] + 1) * k:.2f}  ⚡️ \nСтоимость: {max(100, int(((data[3] + 15) * k - data[3]) * cost))} 💸 \n'
                                                    f'Шанс критического урона: \nБыло: {data[4]:.2f} 🤞🏻 \nСтанет: {data[4] + kk:.2f} 🤞🏻 \nСтоимость: {max(100, int(((data[4] + 25) * k - data[4]) * cost))} 💸',
                                   reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Базовый урон ⚔️':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Money, Experience
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[6]) * 0.2
            money = data[5]
            if money < max(100, int(((data[1] + 5) * k - data[1]) * cost)):
                await bot.send_message(message.chat.id, f'Недостаточно монет(')
            else:
                cur.execute(f"""UPDATE Users SET 
                                                           Experience = {data[1] + max(100, int(((data[1] + 5) * k - data[1]) * cost)) * 0.05} 
                                                           WHERE TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET 
                                       Money = {money - max(100, int(((data[1] + 5) * k - data[1]) * cost))} 
                                       WHERE TG_ID = {user_id}""")
                cur.execute(
                    f"""UPDATE Users SET Base_Attack = {(data[1] + 5) * k} WHERE TG_ID = {user_id}""")
                data = cur.execute(f"""SELECT Base_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                        f'Ваш Базовый урон: {data[0]:.2f} ⚔️\n'
                                                        f'Следующее улучшение: {(data[0] + 5) * k:.2f} ⚔️',
                                       reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Базовая защита 🛡':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Money, Experience
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[6]) * 0.2
            money = data[5]
            if money < max(100, int(((data[2] + 5) * k - data[2]) * cost)):
                await bot.send_message(message.chat.id, f'Недостаточно монет(')
            else:
                cur.execute(f"""UPDATE Users SET 
                                                           Experience = {data[6] + max(100, int(((data[2] + 5) * k - data[2]) * cost)) * 0.05} 
                                                           WHERE TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET 
                                       Money = {money - max(100, int(((data[2] + 5) * k - data[2]) * cost))} 
                                       WHERE TG_ID = {user_id}""")
                cur.execute(
                    f"""UPDATE Users SET Base_Shield = {(data[2] + 5) * k} WHERE TG_ID = {user_id}""")
                data = cur.execute(f"""SELECT Base_Shield, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸 \n'
                                                        f'Ваш Базовая защита: {data[0]:.2f} 🛡\n'
                                                        f'Следующее улучшение: {(data[0] + 5) * k:.2f} 🛡',
                                       reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Максимальное Здоровье ⛑':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Money, Experience
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[6]) * 0.2
            money = data[5]
            if money < max(100, int(((data[0] + 5) * k - data[0]) * cost)):
                await bot.send_message(message.chat.id, f'Недостаточно монет(')
            else:
                cur.execute(f"""UPDATE Users SET 
                               Experience = {data[6] + max(100, int(((data[0] + 5) * k - data[0]) * cost)) * 0.05} 
                               WHERE TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET 
                                       Money = {money - max(100, int(((data[0] + 5) * k - data[0]) * cost))} 
                                       WHERE TG_ID = {user_id}""")
                cur.execute(
                    f"""UPDATE Users SET Max_Health_Points = {(data[0] + 5) * k} WHERE TG_ID = {user_id}""")
                data = cur.execute(f"""SELECT Max_Health_Points, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸 \n'
                                                        f'Ваше Максимальное здоровье: {data[0]:.2f} ⛑\n'
                                                        f'Следующее улучшение: {(data[0] + 5) * k:.2f} ️ ⛑',
                                       reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Критический урон ⚡️':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Money, Experience
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[6]) * 0.2
            money = data[5]
            if money < max(100, int(((data[3] + 15) * k - data[3]) * cost)):
                await bot.send_message(message.chat.id, f'Недостаточно монет(')
            else:
                cur.execute(f"""UPDATE Users SET 
                               Experience = {data[6] + max(100, int(((data[3] + 15) * k - data[3]) * cost)) * 0.05} 
                               WHERE TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET 
                                       Money = {money - max(100, int(((data[3] + 15) * k - data[3]) * cost))} 
                                       WHERE TG_ID = {user_id}""")
                cur.execute(
                    f"""UPDATE Users SET Critical_Attack = {(data[3] + 1) * k} WHERE TG_ID = {user_id}""")
                data = cur.execute(f"""SELECT Critical_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸 \n'
                                                        f'Ваш Критический урон: {data[0]:.2f} ⚡\n️'
                                                        f'Следующее улучшение: {(data[0] + 1) * k:.2f} ⚡',
                                       reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Шанс на Критический удар 🤞🏻':
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Money, Experience
                            FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef(data[6]) * 0.2
            money = data[5]
            if money < max(100, int(((data[4] + 25) * k - data[4]) * cost)):
                await bot.send_message(message.chat.id, f'Недостаточно монет(')
            else:
                cur.execute(f"""UPDATE Users SET 
                               Experience = {data[6] + max(100, int(((data[4] + 25) * k - data[4]) * cost)) * 0.05} 
                               WHERE TG_ID = {user_id}""")
                cur.execute(f"""UPDATE Users SET 
                                       Money = {money - max(100, int(((data[4] + 25) * k - data[4]) * cost))} 
                                       WHERE TG_ID = {user_id}""")
                cur.execute(
                    f"""UPDATE Users SET Critical_Chance = {data[4] + kk} WHERE TG_ID = {user_id}""")
                data = cur.execute(f"""SELECT Critical_Chance, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸 \n'
                                                        f'Ваш шанс на Критический удар: {data[0]:.2f} 🤞🏻\n'
                                                        f'Следующее улучшение: {data[0] + kk:.2f} 🤞🏻',
                                       reply_markup=shop_base_kb)
            cur.execute(
                f"UPDATE Users SET Status = 105 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Стихийные улучшения 🌱':
            #data = cur.execute(
                #f"""SELECT E_Shield, E_Attack, C_Shield, C_Attack, F_Shield, F_Attack, M_Shield, M_Attack,
                            #FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            #k = 1.1
            #kk = 0.001
            #cost = money_coef(data[2]) * 0.2
            #await bot.send_message(message.chat.id, f'Физическая атака: \nБыло {data[1]:.2f} ⚔️ \nСтанет: {(data[1] + 5) * k:.2f} ⚔️\nСтоимость: {max(100, int(((data[1] + 5) * k - data[1]) * cost))} 💸 '
                                                    #f'\nБазовая защита: \nБыло {data[2]:.2f} 🛡 \nСтанет: {(data[2] + 5) * k:.2f} 🛡 \nСтоимость: {max(100, int(((data[2] + 5) * k - data[2]) * cost))} 💸 '
                                                    #f'\nМаксимальное здоровье:\nБыло {data[0]:.2f} ⛑ \nСтанет: {(data[0] + 5) * k:.2f} ⛑ \nСтоимость: {max(100, int(((data[0] + 5) * k - data[0]) * cost))} 💸 '
                                                    #f'\nКритический урон: \nБыло {data[3]:.2f}  ⚡️ \nСтанет: {(data[3] + 1) * k:.2f}  ⚡️ \nСтоимость: {max(100, int(((data[3] + 15) * k - data[3]) * cost))} 💸 \n'
                                                    #f'Шанс критического урона: \nБыло {data[4]:.2f} 🤞🏻 \nСтанет: {data[4] + kk:.2f} 🤞🏻 \nСтоимость: {max(100, int(((data[4] + 25) * k - data[4]) * cost))} 💸'
                                                    #f'\nБазовый урон: \nБыло {data[1]:.2f} ⚔️ \nСтанет: {(data[1] + 5) * k:.2f} ⚔️\nСтоимость: {max(100, int(((data[1] + 5) * k - data[1]) * cost))} 💸 '
                                                    #f'\nБазовая защита: \nБыло {data[2]:.2f} 🛡 \nСтанет: {(data[2] + 5) * k:.2f} 🛡 \nСтоимость: {max(100, int(((data[2] + 5) * k - data[2]) * cost))} 💸 '
                                                    #f'\nМаксимальное здоровье:\nБыло {data[0]:.2f} ⛑ \nСтанет: {(data[0] + 5) * k:.2f} ⛑ \nСтоимость: {max(100, int(((data[0] + 5) * k - data[0]) * cost))} 💸 '
                                                    #f'\nКритический урон: \nБыло {data[3]:.2f}  ⚡️ \nСтанет: {(data[3] + 1) * k:.2f}  ⚡️ \nСтоимость: {max(100, int(((data[3] + 15) * k - data[3]) * cost))} 💸 \n'
                                                    #f'Шанс критического урона: \nБыло {data[4]:.2f} 🤞🏻 \nСтанет: {data[4] + kk:.2f} 🤞🏻 \nСтоимость: {max(100, int(((data[4] + 25) * k - data[4]) * cost))} 💸',
                                   #reply_markup=shop_adv_kb)
            await bot.send_message(message.chat.id, 'Выберите, что хотите улучшить:', reply_markup=fea_kb)
            cur.execute(
                f"UPDATE Users SET Status = 205 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Показатели 🌈':
            user_id = message.from_user.id
            cur.execute(f'''UPDATE Users SET status = {12} WHERE TG_ID = {user_id}''')
            connection.commit()
            data = cur.execute(
                f"""SELECT Max_Health_Points, 
                                        Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, Health_Points, Experience, Money
                                        FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
            if exp_to_level(data[6]) < 3:
                stic = '👶🏻'
            elif exp_to_level(data[6]) >= 3 and exp_to_level(data[6]) < 5:
                stic = '👦🏼'
            elif exp_to_level(data[6]) >= 5 and exp_to_level(data[6]) < 7:
                stic = '👨🏻‍'
            elif exp_to_level(data[6]) >= 7 and exp_to_level(data[6]) < 20:
                stic = '👨🏻‍🦳‍'
            elif exp_to_level(data[6]) >= 20:
                stic = '👹'
            await bot.send_message(message.chat.id, f'Ваш уровень: {exp_to_level(data[6])} {stic}\nВаши монеты: {data[7]} 💸\n'
                                   f'Базовый урон: {data[1]:.2f} ⚔️ \nБазовая защита: {data[2]:.2f} 🛡 \nНастоящее здоровье: {data[5]} ❤️\nМаксимальное здоровье: {data[0]:.2f} ⛑ \nКритический урон: {data[3]:.2f}  ⚡️ \n'
                                   f'Шанс критического урона: \n{data[4]:.2f} 🤞🏻 ')
            cur.execute(
                f"UPDATE Users SET Status = 12 WHERE TG_ID = {user_id}")
            connection.commit()
        elif message.text == 'Физические характеристики 🦾':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                            C_Attack, F_Attack, M_Attack FROM Users 
                                            WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            if status == 205:
                cur.execute(
                    f"UPDATE Users SET Status = 2051 WHERE TG_ID = {user_id}")
                connection.commit()
                await bot.send_message(message.chat.id, f'Физческая атака 🦾:\nБыло:\n{data[5]:.2f} ⚔\nСтанет:\n{(data[5] + 10) * k:.2f} ⚔\nСтоимость:\n{max(100, int(((data[5] + 10) * k - data[5]) * cost))} монет💸\n'
                                                        f'Физическая защита 🦾:\nБыло:\n{data[0]:.2f} 🛡\nСтанет:\n{(data[0] + 10) * k:.2f} 🛡\nСтоимость:\n{max(100, int(((data[0] + 10) * k - data[0]) * cost))} монет💸',
                                       reply_markup=aors_kb)
                await bot.send_message(message.chat.id, 'Выберете, что улучшить:')
            else:
                fea_E = cur.execute(f'''SELECT E_Shield, E_Attack FROM Users WHERE TG_ID = {user_id}''').fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Ваша Физическая атака: {fea_E[1]:.2f} ⚔ \n'
                                       f'Ваша Физческая защита: {fea_E[0]:.2f} 🛡',
                                       reply_markup=fea_kb)
        elif message.text == 'Криогенные характеристики 🧊':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                        WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            if status == 205:
                cur.execute(
                    f"UPDATE Users SET Status = 2052 WHERE TG_ID = {user_id}")
                connection.commit()
                await bot.send_message(message.chat.id,
                                       f'Криогенная атака 🧊:\nБыло:\n{data[6]:.2f} ⚔\nСтанет:\n{(data[6] + 10) * k:.2f} ⚔\nСтоимость:\n{max(100, int(((data[6] + 10) * k - data[5]) * cost))} монет💸\n'
                                       f'Криогенная защита 🧊:\nБыло:\n{data[1]:.2f} 🛡\nСтанет:\n{(data[1] + 10) * k:.2f} 🛡\nСтоимость:\n{max(100, int(((data[1] + 10) * k - data[0]) * cost))} монет💸',
                                       reply_markup=aors_kb)
                await bot.send_message(message.chat.id, 'Выберете, что улучшить:')
            else:
                fea_E = cur.execute(f'''SELECT C_Shield, C_Attack FROM Users WHERE TG_ID = {user_id}''').fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Ваша Криогенная атака: {fea_E[1]:.2f} ⚔ \n'
                                       f'Ваша Криогенная защита: {fea_E[0]:.2f} 🛡',
                                       reply_markup=fea_kb)
        elif message.text == 'Огненные характеристики 🔥':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                        WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            if status == 205:
                cur.execute(
                    f"UPDATE Users SET Status = 2053 WHERE TG_ID = {user_id}")
                connection.commit()
                await bot.send_message(message.chat.id,
                                       f'Огненная атака 🔥:\nБыло:\n{data[7]:.2f} ⚔\nСтанет:\n{(data[7] + 10) * k:.2f} ⚔\nСтоимость:\n{max(100, int(((data[7] + 10) * k - data[7]) * cost))} монет💸\n'
                                       f'Огненная защита 🔥:\nБыло:\n{data[3]:.2f} 🛡\nСтанет:\n{(data[3] + 10) * k:.2f} 🛡\nСтоимость:\n{max(100, int(((data[3] + 10) * k - data[3]) * cost))} монет💸',
                                       reply_markup=aors_kb)
                await bot.send_message(message.chat.id, 'Выберете, что улучшить:')
            else:
                fea_E = cur.execute(f'''SELECT F_Shield, F_Attack FROM Users WHERE TG_ID = {user_id}''').fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Ваша Огненная атака: {fea_E[1]:.2f} ⚔ \n'
                                       f'Ваша Огненная защита: {fea_E[0]:.2f} 🛡',
                                       reply_markup=fea_kb)
        elif message.text == 'Магические характеристики 🔮':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                                        C_Attack, F_Attack, M_Attack FROM Users 
                                                        WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            if status == 205:
                cur.execute(
                    f"UPDATE Users SET Status = 2054 WHERE TG_ID = {user_id}")
                connection.commit()
                await bot.send_message(message.chat.id,
                                       f'Магическая атака 🔮:\nБыло:\n{data[8]:.2f} ⚔\nСтанет:\n{(data[8] + 10) * k:.2f} ⚔\nСтоимость:\n{max(100, int(((data[8] + 10) * k - data[8]) * cost))} монет💸\n'
                                       f'Магическая защита 🔮:\nБыло:\n{data[4]:.2f} 🛡\nСтанет:\n{(data[4] + 10) * k:.2f} 🛡\nСтоимость:\n{max(100, int(((data[4] + 10) * k - data[4]) * cost))} монет💸',
                                       reply_markup=aors_kb)
                await bot.send_message(message.chat.id, 'Выберете, что улучшить:')
            else:
                fea_E = cur.execute(f'''SELECT M_Shield, M_Attack FROM Users WHERE TG_ID = {user_id}''').fetchall()[0]
                connection.commit()
                await bot.send_message(message.chat.id, f'Ваша Магическая атака: {fea_E[1]:.2f} ⚔ \n'
                                       f'Ваша Магическая защита: {fea_E[0]:.2f} 🛡',
                                       reply_markup=fea_kb)
        elif message.text == 'Атака ⚔️':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                                                    C_Attack, F_Attack, M_Attack, Money FROM Users 
                                                                    WHERE TG_ID = {user_id}""").fetchall()[0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            money = data[-1]
            if status == 2051:
                if money < max(100, int(((data[5] + 10) * k - data[5]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                Experience = {data[2] + max(100, int(((data[5] + 10) * k - data[5]) * cost)) * 0.05} 
                                                                WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                            Money = {money - max(100, int(((data[5] + 10) * k - data[5]) * cost))} 
                                            WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET E_Attack = {(data[5] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT E_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваш Физический урон: {data[0]:.2f} ⚔\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} ⚔')
            if status == 2052:
                if money < max(100, int(((data[6] + 10) * k - data[6]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                Experience = {data[2] + max(100, int(((data[6] + 10) * k - data[6]) * cost)) * 0.05} 
                                                                WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                            Money = {money - max(100, int(((data[6] + 10) * k - data[6]) * cost))} 
                                            WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET C_Attack = {(data[6] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT C_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваш Криогенный урон: {data[0]:.2f} ⚔️\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} ⚔')
            if status == 2053:
                if money < max(100, int(((data[7] + 10) * k - data[7]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                Experience = {data[2] + max(100, int(((data[7] + 10) * k - data[7]) * cost)) * 0.05} 
                                                                WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                            Money = {money - max(100, int(((data[7] + 10) * k - data[7]) * cost))} 
                                            WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET F_Attack = {(data[7] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT F_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваш Огненный урон: {data[0]:.2f} ⚔️\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} ⚔')
            if status == 2054:
                if money < max(100, int(((data[8] + 10) * k - data[8]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                Experience = {data[2] + max(100, int(((data[8] + 10) * k - data[8]) * cost)) * 0.05} 
                                                                WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                            Money = {money - max(100, int(((data[8] + 10) * k - data[8]) * cost))} 
                                            WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET M_Attack = {(data[8] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT M_Attack, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваш Магический урон: {data[0]:.2f} ⚔\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} ⚔')
        elif message.text == 'Защита 🛡':
            status = cur.execute(f'''SELECT status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]
            user_id = message.from_user.id
            data = cur.execute(f"""SELECT E_Shield, C_Shield, Experience, F_Shield, M_Shield, E_Attack, 
                                                                                C_Attack, F_Attack, M_Attack, Money FROM Users 
                                                                                WHERE TG_ID = {user_id}""").fetchall()[
                0]
            k = 1.1
            kk = 0.001
            cost = money_coef((data[2]) * 0.1)
            money = data[-1]
            if status == 2051:
                if money < max(100, int(((data[0] + 10) * k - data[0]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                            Experience = {data[2] + max(100, int(((data[0] + 10) * k - data[0]) * cost)) * 0.05} 
                                                                            WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                                        Money = {money - max(100, int(((data[0] + 10) * k - data[0]) * cost))} 
                                                        WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET E_Shield = {(data[0] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT E_Shield, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваша Физическая защита: {data[0]:.2f} 🛡\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} 🛡')
            if status == 2052:
                if money < max(100, int(((data[1] + 10) * k - data[1]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                            Experience = {data[2] + max(100, int(((data[1] + 10) * k - data[1]) * cost)) * 0.05} 
                                                                            WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                                        Money = {money - max(100, int(((data[1] + 10) * k - data[1]) * cost))} 
                                                        WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET C_Shield = {(data[1] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT C_Shield, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваша Криогенная защита: {data[0]:.2f} 🛡\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} 🛡')
            if status == 2053:
                if money < max(100, int(((data[3] + 10) * k - data[3]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                            Experience = {data[2] + max(100, int(((data[3] + 10) * k - data[3]) * cost)) * 0.05} 
                                                                            WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                                        Money = {money - max(100, int(((data[3] + 10) * k - data[7]) * cost))} 
                                                        WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET F_Shield = {(data[3] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT F_Shield, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()

                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваша Огненная защита: {data[0]:.2f} 🛡\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} 🛡')
            if status == 2054:
                if money < max(100, int(((data[4] + 10) * k - data[4]) * cost)):
                    await bot.send_message(message.chat.id, f'Недостаточно монет(')
                else:
                    cur.execute(f"""UPDATE Users SET 
                                                                            Experience = {data[2] + max(100, int(((data[4] + 10) * k - data[4]) * cost)) * 0.05} 
                                                                            WHERE TG_ID = {user_id}""")
                    cur.execute(f"""UPDATE Users SET 
                                                        Money = {money - max(100, int(((data[4] + 10) * k - data[4]) * cost))} 
                                                        WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET M_Shield = {(data[4] + 10) * k} WHERE TG_ID = {user_id}""")
                    data = cur.execute(f"""SELECT M_Shield, Money FROM Users WHERE TG_ID = {user_id}""").fetchall()[0]
                    connection.commit()
                    await bot.send_message(message.chat.id, f'Успех. Монеты: {data[-1]} 💸\n'
                                                            f'Ваша Магическая защита: {data[0]:.2f} 🛡\n️'
                                                            f'Следующее улучшение: {(data[0] + 10) * k:.2f} 🛡')
        elif cur.execute(f'''SELECT Status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0] == 60:
            await bot.send_message(message.chat.id, f'*Промах*', parse_mode='Markdown', reply_markup=fight_kb)
            data = cur.execute(
                f"""SELECT User_Name, Rating, Experience, 
                                                            Money, Health_Points, Max_Health_Points, 
                                                            Base_Attack, Base_Shield, Critical_Attack, Critical_Chance, 
                                                            E_Shield, C_Shield, F_Shield, M_Shield, E_Attack, 
                                                            C_Attack, F_Attack, M_Attack FROM Users 
                                                            WHERE TG_ID = {user_id}""").fetchall()[
                0]
            enemy_id = cur.execute(
                f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
            enemy_hp = cur.execute(
                f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy_hp_max = cur.execute(
                f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            enemy_attack = cur.execute(
                f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                0][0]
            await bot.send_message(message.chat.id, f'ВАС АТАКУЕТ *{enemy[1]}*\n\n'
                                                    f'_Здоровье_: *{enemy_hp} ❤️/ {enemy_hp_max} ❤️*\n'
                                                    f'_Базовый урон_: *{enemy_attack:.2f}*\n',
                                   parse_mode='Markdown')
            hp = data[4]
            chance = random.randint(1, 100)
            if chance <= 10:
                await bot.send_message(message.chat.id, f'ФУХ, враг *промахнулся*', parse_mode='Markdown')
            elif chance >= 90 and enemy_hp != enemy_hp_max:
                await bot.send_message(message.chat.id, f'Враг *подлечился* ⛑', parse_mode='Markdown')
                cur.execute(f"""UPDATE Users SET Current_Enemy_HP = {enemy_hp} WHERE TG_ID = {user_id}""")
                connection.commit()
            else:
                shield = \
                    cur.execute(
                        f"""SELECT {enemy[2]}_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                shield_all = cur.execute(
                    f"""SELECT Base_Shield FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                    0][0]
                hp = hp + min(-int(enemy_attack * 0.1), -enemy_attack + shield + shield_all)
                await bot.send_message(message.chat.id,
                                       f'_Враг нанес вам урон_: *{-min(int(enemy_attack * 0.1), -enemy_attack + shield + shield_all):.2f} ❤*\n'
                                       f'_Ваше здоровье_: *{max(0, hp)} ❤️/ {data[5]} ❤️*', parse_mode='Markdown')
                if hp < 1:
                    cur.execute(
                        f"""UPDATE Users SET Health_Points = {int(data[5])} WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET Experience = {int(data[2] * 0.9)} WHERE TG_ID = {user_id}""")
                    cur.execute(
                        f"""UPDATE Users SET Rating = {max(0, data[1] - enemy[8] * 30)} WHERE TG_ID = {user_id}""")
                    connection.commit()
                    await bot.send_message(message.chat.id, f'*Вы проиграли* ☠️\n\n'
                                                            f'Вы потеряли:\n'
                                                            f'_Опыт_: *{data[2] - int(data[2] * 0.9)}* ⭐️\n'
                                                            f'_Очки Рейтинга_: *{data[1] - max(0, data[1] - enemy[8] * 30)}* 🏆\n'
                                                            f'\n'
                                                            f'_Ваше здоровье восполненно_', reply_markup=menu_kb,
                                           parse_mode='Markdown')

                    cur.execute(f"""UPDATE Users SET Status = 1 WHERE TG_ID = {user_id}""")
                    connection.commit()
                else:
                    cur.execute(f"""UPDATE Users SET Health_Points = {int(hp)} WHERE TG_ID = {user_id}""")
                    enemy_id = cur.execute(
                        f"""SELECT Current_Enemy_ID FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    enemy = cur.execute(f"""SELECT * FROM Slimes WHERE Enemy_ID = {enemy_id}""").fetchall()[0]
                    enemy_hp = cur.execute(
                        f"""SELECT Current_Enemy_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    enemy_hp_max = cur.execute(
                        f"""SELECT Current_Enemy_Max_HP FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    enemy_attack = cur.execute(
                        f"""SELECT Current_Enemy_Attack FROM Users WHERE TG_ID = {user_id}""").fetchall()[
                        0][0]
                    connection.commit()
        #elif cur.execute(f'''SELECT Status FROM Users WHERE TG_ID = {user_id}''').fetchall()[0][0]:

            #await bot.send_message(message.chat.id, f'Добро пожаловать, {username}!', reply_markup=menu_kb)
        else:
            await bot.send_message(message.chat.id, f'_Меню_', parse_mode='Markdown', reply_markup=menu_kb)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
