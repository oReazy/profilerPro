# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time, hashlib

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class editname(LS):
    tName = ''
    tSurname = ''

    tNameEditColor = 'black'

    async def unMouseName(self):
        self.tNameEditColor = 'black'

    async def onMouseName(self):
        self.tNameEditColor = 'blue'

    async def onClickButton(self):
        args = self.router.page.params['id']
        await database.setData('pages', 'id', f"'{args}'", 'name', f"'{self.tName}'")
        await database.setData('pages', 'id', f"'{args}'", 'surname', f"'{self.tSurname}'")

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def editName():
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon('pencil', size=20, margin_left='6px', on_mouse_enter=editname.onMouseName, on_mouse_leave=editname.unMouseName, color=rx.color(editname.tNameEditColor, 9))),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8_add_user_male.svg', width='25px'),
                        rx.text('Изменение имени и фамилии', font_family='SFProDisplayBold', size='3'),
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
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=editname.tName,
                    on_change=[editname.set_tName],
                    font_family='SFProDisplayBold',
                    placeholder='Имя',
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=editname.tSurname,
                    on_change=[editname.set_tSurname],
                    font_family='SFProDisplayBold',
                    placeholder='Фамилия',
                ),
                rx.button('Сохранить', font_family='SFProDisplayBold', on_click=editname.onClickButton),
                spacing='2',
                direction='column'
            ),
            width='400px'
        ),
    )