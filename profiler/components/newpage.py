# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time, hashlib

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class newpage(LS):
    tName = ''

    tButtonDisable = True
    tButtonLoading = False
    tNameDisable = False

    tErrorVision = False
    tErrorText = ''

    async def onClickButton(self):
        self.tButtonDisable = True
        self.tButtonLoading = True
        self.tNameDisable = True
        USER = await database.getUserHash(f"'{self.HASH}'")
        ID = USER[0]
        IMAGES = ['/images/pages/avatar.png', '/images/pages/wallpaper.png']
        VISION = [True, False, False, False, True]
        await database.addNewData(
            'pages',
            'name, surname, pages, description, portfolio, experienceJob, links, priority, icons, images, url, private, banReason, idAuthor, dateCreate, namePage, vision',
            f"'', '', '[]', '', '[]', '[]', '[]', '[]', '[]', \"{IMAGES}\", '', '1', '', '{ID}', '{time.time()}', '{self.tName}', \"{VISION}\""
        )
        row = await database.getData('pages', 'idAuthor', f'"{ID}"')
        ID = row[0]
        return rx.redirect(f'/page/edit/{ID}')

    async def onStart(self):
        self.tName = ''
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tNameDisable = False
        self.tErrorVision = False
        self.tErrorText = ''

    async def checkForm(self):
        if self.tName != '':
            self.tButtonDisable = False
        else:
            self.tButtonDisable = True


# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index(size):
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Создать', font_family='SFProDisplayBold', size=size, on_click=newpage.onStart)),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8_add_user_male.svg', width='25px'),
                        rx.text('Создать страницу', font_family='SFProDisplayBold', size='3'),
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
                    newpage.tErrorVision,
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.icon('triangle-alert', color=rx.color('tomato', 9)),
                                rx.text(newpage.tErrorText, font_family='SFProDisplayMedium'),
                                direction='row',
                                align='center',
                                spacing='2',
                            ),
                            background=rx.color('tomato', 5)
                        ),
                        rx.divider(margin_top='8px'),
                        direction='column'
                    ),
                ),
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=newpage.tName,
                    on_change=[newpage.set_tName, newpage.checkForm],
                    disabled=newpage.tNameDisable,
                    font_family='SFProDisplayBold',
                    placeholder='Название страницы',
                ),
                rx.button('Создать страницу', font_family='SFProDisplayBold', disabled=newpage.tButtonDisable, loading=newpage.tButtonLoading, on_click=newpage.onClickButton),
                spacing='2',
                direction='column'
            ),
            width='400px'
        ),
    )