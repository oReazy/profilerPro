"""

[ LOCALSTORAGE ]

Версия: 2.0-A | Последнее изменение: 02.01.2025

[2.0-A: Бета-версия обновления: изменения в локальном хранилище: переименование данных, улучшенное взаимодействие между функциями и беком]
[1.0: Введено в проект, введены базовые принципы]

"""

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from typing import Union, Tuple
from rxconfig import config

# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class Storage(rx.State):

    # Переменные, которые необходимо сохранять в localStorage и использовать их в будущем
    HASH: str = rx.LocalStorage('0', name='hash') # Хэш игрока, хранится всегда в localStorage

    # Глобальные переменные, их всегда необходимо использовать при необходимости
    USER = () # Хранение данных об игроке
    SERVER = () # Хранение данных об сервере

    tPortfolio: list[list[str]]
    tPortfolioCount = 0

    tLinks: list[list[str]]
    tLinksCount = 0

    style = {"text-decoration": "none !important",  # Убираем подчёркивание
             "color": "inherit !important",  # Цвет наследуется от родителя
             "cursor": "hover",  # Убираем указатель на ссылке
             "outline": 'none',
             }
    hover = {"color": "inherit !important",  # Цвет не меняется при наведении
             "text-decoration": "none !important",  # Подчёркивание не появляется
             "background-color": "transparent !important",  # Чтобы исключить изменения фона
             }
    style2 = {
        "object-fit": "cover",  # Покрытие всей области
        "object-position": "center",  # Центровка изображения
    }

    async def onLoad(self):
        self.SERVER = await database.getData('settings', 'id', '1')  # Получаем данные с сервера
        if self.SERVER[5] == 1:
            if self.HASH != '0':
                tUserCount = await database.getDataMultiCount('users', 'hash', f"'{self.HASH}'")  # Получаем количество игроков с таким хэшем
                if tUserCount != 0:
                    self.USER = await database.getUserHash(f"'{self.HASH}'")  # Устанавливаем данные игрока из его хэша
                else:
                    # Игрок с HASH не найден, необходимо тут сбросить хэш на 0 и оптравить человека на главную страницу
                    return [rx.clear_local_storage(), rx.redirect('/')]
            else:
                # Игрок просто не авторизован, переброс на главную страницу
                return rx.redirect('/')
        else:
            # Сервер в этом случае закрыт, переброс на страницу we'll be right back
            return rx.redirect('/we-be-right-back')


    async def onLoadLite(self):
        self.SERVER = await database.getData('settings', 'id', '1')  # Получаем данные с сервера
        if self.SERVER[5] == 1:
            if self.HASH != '0':
                tUserCount = await database.getDataMultiCount('users', 'hash', f"'{self.HASH}'")  # Получаем количество игроков с таким хэшем
                if tUserCount != 0:
                    self.USER = await database.getUserHash(f"'{self.HASH}'")  # Устанавливаем данные игрока из его хэша
                else:
                    # Игрок с HASH не найден, необходимо тут сбросить хэш на 0 и оптравить человека на главную страницу
                    return [rx.clear_local_storage()]
        else:
            # Сервер в этом случае закрыт, переброс на страницу we'll be right back
            return rx.redirect('/we-be-right-back')