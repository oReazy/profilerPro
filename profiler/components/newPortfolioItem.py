# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time, hashlib, pathlib

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class newPortfolioItem(LS):
    tName = ''
    tTitle = ''
    tDescription = ''


    tButtonDisable = True
    tButtonLoading = False

    tErrorVision = False
    tErrorText = ''
    tImage = '/images/pages/portfolio120.png'

    async def onClickButton(self):
        pass

    async def onStart(self):
        self.tName = ''
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tErrorVision = False
        self.tErrorText = ''

    async def checkForm(self):
        if self.tName != '':
            self.tButtonDisable = False
        else:
            self.tButtonDisable = True

    async def unMouseImgae(self):
        if self.tImage == '/images/pages/portfolio120_alt.png':
            self.tImage = '/images/pages/portfolio120.png'

    async def onMouseImage(self):
        if self.tImage == '/images/pages/portfolio120.png':
            self.tImage = '/images/pages/portfolio120_alt.png'

    @rx.event
    async def handle_upload_portfolio(self, files: list[rx.UploadFile]):
        # Указываем путь к папке TEST
        args = self.router.page.params['id']
        upload_dir = pathlib.Path(f"uploaded_files/{args}/portfolio")

        # Создаем папку, если она не существует
        upload_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            upload_data = await file.read()

            # Указываем путь для сохранения файла в папке TEST
            outfile = upload_dir / file.filename

            # Сохраняем файл
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Обновляем переменную
            self.tImages[0] = f'/{args}/{file.filename}'
            args = self.router.page.params['id']
            await database.setData('pages', 'id', f"'{args}'", 'images', f'\"{self.tImages}\"')
            self.USER = await database.getUserHash(f"'{self.HASH}'")

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index():
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Добавить работу', font_family='SFProDisplayBold', size='1')),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8-choose_page.svg', width='25px'),
                        rx.text('Добавить работу в портфолио', font_family='SFProDisplayBold', size='3'),
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
                rx.flex(
                    rx.flex(
                        rx.text('Заголовок', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newPortfolioItem.tName,
                            on_change=[newPortfolioItem.set_tName],
                            font_family='SFProDisplayBold',
                            placeholder='Название вашей работы',
                            width='255px'
                        ),
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Краткое описание', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newPortfolioItem.tName,
                            on_change=[newPortfolioItem.set_tName],
                            font_family='SFProDisplayBold',
                            placeholder='Название вашей работы',
                            width='255px'
                        ),
                        direction='column',
                        spacing='2'
                    ),
                    direction='row',
                    spacing='2'
                ),
                spacing='2',
                direction='column'
            ),
            width='700px'
        ),
    )