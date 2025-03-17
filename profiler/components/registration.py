
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class registration(LS):
    tLogin = ''
    tPassword = ''
    tEmail = ''
    
    tButtonDisable = False
    tButtonLoading = False

    tErrorVision = False
    tErrorText = ''

    tLoginDisable = False
    tPasswordDisable = False
    tEmailDisable = False

    async def onClickButton(self):
        self.tButtonDisable = True
        self.tButtonLoading = True
        self.tLoginDisable = True
        self.tPasswordDisable = True
        self.tEmailDisable = True
        countLogins = await database.getDataMultiCount('users', 'nick', f"'{self.tLogin}'")
        countEmails = await database.getDataMultiCount('users', 'email', f"'{self.tEmail}'")
        if countLogins == 0:
            if countEmails == 0:
                await database.addNewAccount(self.tLogin, self.tPassword, self.tEmail)
                USER = await database.getData('users', 'nick', f"'{self.tLogin}'")
                self.HASH = USER[2]
                self.USER = await database.getUserHash(f"'{self.HASH}'")
                return rx.redirect('/mypages')
            else:
                self.tErrorVision = True
                self.tErrorText = 'Почта уже используется'
                self.tButtonDisable = False
                self.tButtonLoading = False
                self.tLoginDisable = False
                self.tPasswordDisable = False
                self.tEmailDisable = False
        else:
            self.tErrorVision = True
            self.tErrorText = 'Логин уже используется'
            self.tButtonDisable = False
            self.tButtonLoading = False
            self.tLoginDisable = False
            self.tPasswordDisable = False
            self.tEmailDisable = False

    async def checkForm(self):
        if self.tLogin != '' and self.tPassword != '' and self.tEmail != '':
            self.tButtonDisable = False
        else:
            self.tButtonDisable = True

    async def onStart(self):
        self.tLogin = ''
        self.tPassword = ''
        self.tEmail = ''
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tButtonLoading = False
        self.tLoginDisable = False
        self.tPasswordDisable = False
        self.tEmailDisable = False

        self.tErrorVision = False
        self.tErrorText = ''

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index(size):
    return rx.dialog.root(
    rx.dialog.trigger(rx.button('Зарегистрироваться', font_family='SFProDisplayBold', size=size, on_click=registration.onStart)),
    rx.dialog.content(
        rx.flex(
            rx.flex(
                rx.flex(
                    rx.image('/icons/icons8_add_user_male.svg', width='25px'),
                    rx.text('Регистрация', font_family='SFProDisplayBold', size='3'),
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
                registration.tErrorVision,
                rx.flex(
                    rx.card(
                        rx.flex(
                            rx.icon('triangle-alert', color=rx.color('tomato', 9)),
                            rx.text(registration.tErrorText, font_family='SFProDisplayMedium'),
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
                value=registration.tLogin,
                on_change=[registration.set_tLogin, registration.checkForm],
                disabled=registration.tLoginDisable,
                font_family='SFProDisplayBold',
                placeholder='Логин',
            ),
            rx.input(
                rx.input.slot(
                    rx.icon('lock', size=17, color=rx.color('gray', 9))
                ),
                value=registration.tPassword,
                on_change=[registration.set_tPassword, registration.checkForm],
                disabled=registration.tPasswordDisable,
                type='password',
                font_family='SFProDisplayBold',
                placeholder='Пароль'
            ),
            rx.input(
                rx.input.slot(
                    rx.icon('mail', size=17, color=rx.color('gray', 9))
                ),
                value=registration.tEmail,
                on_change=[registration.set_tEmail, registration.checkForm],
                disabled=registration.tEmailDisable,
                type='email',
                font_family='SFProDisplayBold',
                placeholder='Почта'
            ),
            rx.button('Зарегистрироваться', font_family='SFProDisplayBold', disabled=registration.tButtonDisable, loading=registration.tButtonLoading, on_click=registration.onClickButton),
            spacing='2',
            direction='column'
        ),
        width='400px'
    ),
)