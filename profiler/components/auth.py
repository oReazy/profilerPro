# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time, hashlib

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class auth(LS):
    tLogin = ''
    tPassword = ''

    tButtonDisable = False
    tButtonLoading = False

    tErrorVision = False
    tErrorText = ''

    tLoginDisable = False
    tPasswordDisable = False

    async def onClickButton(self):
        self.tButtonDisable = True
        self.tButtonLoading = True
        self.tLoginDisable = True
        self.tPasswordDisable = True
        countLogins = await database.getDataMultiCount('users', 'nick', f"'{self.tLogin}'")
        if countLogins != 0:
            data_bytes = self.tPassword.encode('utf-8')
            hash_obj = hashlib.sha256(data_bytes)
            hash_hex = hash_obj.hexdigest()
            USER = await database.getData('users', 'nick', f"'{self.tLogin}'")
            if USER[1] == hash_hex:
                self.HASH = USER[2]
                self.USER = await database.getUserHash(f"'{self.HASH}'")
            else:
                self.tErrorVision = True
                self.tErrorText = 'Неверный пароль'
                self.tButtonDisable = False
                self.tButtonLoading = False
                self.tLoginDisable = False
                self.tPasswordDisable = False
        else:
            self.tErrorVision = True
            self.tErrorText = 'Пользователя не существует'
            self.tButtonDisable = False
            self.tButtonLoading = False
            self.tLoginDisable = False
            self.tPasswordDisable = False

    async def checkForm(self):
        if self.tLogin != '' and self.tPassword != '':
            self.tButtonDisable = False
        else:
            self.tButtonDisable = True

    async def onStart(self):
        self.tLogin = ''
        self.tPassword = ''
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tLoginDisable = False
        self.tPasswordDisable = False

        self.tErrorVision = False
        self.tErrorText = ''


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index(size):
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Войти', font_family='SFProDisplayBold', size=size, on_click=auth.onStart)),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8-key.svg', width='25px'),
                        rx.text('Авторизация', font_family='SFProDisplayBold', size='3'),
                        spacing='2',
                        direction='row',
                        align='center'
                    ),
                    rx.flex(
                        rx.badge('Esc', color_scheme='gray', variant="soft", font_family='SFProDisplayBold'),
                        spacing='2',
                        direction='row',
                        align='center'
                    ),
                    spacing='2',
                    direction='row',
                    align='center',
                    justify='between'
                ),
                rx.divider(margin_top='12px'),
                rx.cond(
                    auth.tErrorVision,
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.icon('triangle-alert', color=rx.color('tomato', 9)),
                                rx.text(auth.tErrorText, font_family='SFProDisplayMedium'),
                                direction='row',
                                align='center',
                                spacing='2',
                            ),
                            background=rx.color('tomato', 5)
                        ),
                        rx.divider(margin_top='8px'),
                        direction='column'
                    )
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=auth.tLogin,
                    on_change=[auth.set_tLogin, auth.checkForm],
                    disabled=auth.tLoginDisable,
                    font_family='SFProDisplayBold',
                    placeholder='Логин',
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon('lock', size=17, color=rx.color('gray', 9))
                    ),
                    value=auth.tPassword,
                    on_change=[auth.set_tPassword, auth.checkForm],
                    disabled=auth.tPasswordDisable,
                    type='password',
                    font_family='SFProDisplayBold',
                    placeholder='Пароль'
                ),
                rx.button('Войти', font_family='SFProDisplayBold', disabled=auth.tButtonDisable, loading=auth.tButtonLoading, on_click=auth.onClickButton),
                spacing='2',
                direction='column'
            ),
            width='400px'
        ),
    )