# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time, hashlib, pathlib

from sqlalchemy.testing import rowset

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS
from profiler.states.edit import State as editor

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class newLinkItem(LS):
    tName = ''
    tTitle = ''
    tDescription = ''
    tLink = ''
    tIndex = 0


    tButtonDisable = True
    tButtonLoading = False

    tErrorVision = False
    tErrorText = ''
    tImage = 'Ссылка'


    async def delete(self, item):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        links = list(links)
        index = links.index(item)
        links.pop(index)
        await database.setData('pages', 'id', f"'{args}'", 'links', f'\"{links}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        self.tLinks = list(links)


    async def onStart(self):
        self.tName = ''
        self.tTitle = ''
        self.tDescription = ''
        self.tLink = ''
        self.tImage = 'Ссылка'
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tErrorVision = False
        self.tErrorText = ''

    async def loadItem(self, item):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        links = list(links)
        self.tIndex = links.index(item)
        self.tName = item[0]
        self.tTitle = item[1]
        self.tDescription = item[2]
        self.tLink = item[3]
        self.tImage = item[4]
        self.tButtonDisable = False
        self.tButtonLoading = False
        self.tErrorVision = False
        self.tErrorText = ''

    async def editItem(self):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        links = list(links)
        links[self.tIndex] = [self.tName, self.tTitle, self.tDescription, self.tLink, self.tImage]
        await database.setData('pages', 'id', f"'{args}'", 'links', f'\"{links}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        self.tLinks = list(links)

    async def createItem(self):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        links = list(links)
        links.append([self.tName, self.tTitle, self.tDescription, self.tLink, self.tImage])
        await database.setData('pages', 'id', f"'{args}'", 'links', f'\"{links}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        links = ast.literal_eval(PAGE[7])
        self.tLinks = list(links)



    async def checkForm(self):
        if self.tName != '' and self.tTitle != '' and self.tDescription != '' and self.tLink != '':
            self.tButtonDisable = False
        else:
            self.tButtonDisable = True

    @rx.event
    async def handle_upload_portfolio(self, files: list[rx.UploadFile]):
        # Указываем путь к папке TEST
        args = self.router.page.params['id']
        upload_dir = pathlib.Path(f"uploaded_files/{args}/links")

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
            self.tImage = f'/{args}/links{file.filename[1:]}'

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index():
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Добавить ссылку', font_family='SFProDisplayBold', size='1', on_click=newLinkItem.onStart)),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8-choose_page.svg', width='25px'),
                        rx.text('Добавить ссылку', font_family='SFProDisplayBold', size='3'),
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
                    value=newLinkItem.tName,
                    on_change=[newLinkItem.set_tName, newLinkItem.checkForm],
                    font_family='SFProDisplayBold',
                    placeholder='Название вашей ссылки (видно только вам)',
                    width='100%'
                ),
                rx.divider(),
                rx.flex(
                    rx.flex(
                        rx.text('Заголовок', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tTitle,
                            on_change=[newLinkItem.set_tTitle, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Заголовок вашей ссылки',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Краткое описание', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tDescription,
                            on_change=[newLinkItem.set_tDescription, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Напишите краткое ссылки',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    direction='row',
                    spacing='2'
                ),
                rx.flex(
                    rx.flex(
                        rx.text('Ссылка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tLink,
                            on_change=[newLinkItem.set_tLink, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Ссылка',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Иконка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.flex(
                            rx.match(
                                newLinkItem.tImage,
                                ("Ссылка", rx.icon("square-arrow-out-up-right")),
                                ("Сообщение", rx.icon("message-circle")),
                                ("Бот", rx.icon("bot")),
                                ("Наушники", rx.icon("headphones")),
                                ("Диск", rx.icon("disc")),
                                ("Картинка", rx.icon("image")),
                                ("Twitch", rx.icon("twitch")),
                                ("YouTube", rx.icon("youtube")),
                                ("Instagram", rx.icon("instagram")),
                                ("Dribbble", rx.icon("dribbble")),
                                ("Github", rx.icon("github")),
                                ("Стрелка вправо", rx.icon("circle-arrow-right")),
                            ),
                            rx.select(
                                [f"Ссылка", "Сообщение", "Бот", 'Наушники', 'Диск', 'Картинка', 'Twitch', 'YouTube', 'Instagram', 'Dribbble', 'Github', 'Стрелка вправо'],
                                width='250px',
                                default_value='Ссылка',
                                value=newLinkItem.tImage,
                                on_change=newLinkItem.set_tImage
                            ),
                            align='center',
                            direction='row',
                            spacing='2'
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    margin_top='8px',
                    direction='row',
                    spacing='2'
                ),
                rx.divider(),
                rx.flex(
                    rx.flex(),
                    rx.flex(
                        rx.button('Очистить данные', variant='surface', color_scheme='blue', on_click=newLinkItem.onStart),
                        rx.dialog.close(rx.button('Добавить', disabled=newLinkItem.tButtonDisable, on_click=newLinkItem.createItem)),
                        direction='row',
                        align='center',
                        spacing='2'
                    ),
                    direction='row',
                    justify='between',
                    align='center',
                    spacing='2'
                ),
                spacing='2',
                direction='column'
            ),
            width='700px'
        ),
    )


def openItem(item):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.link(
                rx.flex(
                    rx.match(
                        item[4],
                        ("Ссылка", rx.icon("square-arrow-out-up-right")),
                        ("Сообщение", rx.icon("message-circle")),
                        ("Бот", rx.icon("bot")),
                        ("Наушники", rx.icon("headphones")),
                        ("Диск", rx.icon("disc")),
                        ("Картинка", rx.icon("image")),
                        ("Twitch", rx.icon("twitch")),
                        ("YouTube", rx.icon("youtube")),
                        ("Instagram", rx.icon("instagram")),
                        ("Dribbble", rx.icon("dribbble")),
                        ("Github", rx.icon("github")),
                        ("Стрелка вправо", rx.icon("circle-arrow-right")),
                    ),
                    rx.text(item[0], font_family='SFProDisplayBold'),
                    spacing='2',
                    direction='row',
                    align='center'
                ),
                width='800px',
                style=LS.hover,
                on_click=[newLinkItem.loadItem(item)]
            ),
        ),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8-choose_page.svg', width='25px'),
                        rx.text('Добавить ссылку', font_family='SFProDisplayBold', size='3'),
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
                    value=newLinkItem.tName,
                    on_change=[newLinkItem.set_tName, newLinkItem.checkForm],
                    font_family='SFProDisplayBold',
                    placeholder='Название вашей ссылки (видно только вам)',
                    width='100%'
                ),
                rx.divider(),
                rx.flex(
                    rx.flex(
                        rx.text('Заголовок', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tTitle,
                            on_change=[newLinkItem.set_tTitle, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Заголовок вашей ссылки',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Краткое описание', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tDescription,
                            on_change=[newLinkItem.set_tDescription, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Напишите краткое ссылки',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    direction='row',
                    spacing='2'
                ),
                rx.flex(
                    rx.flex(
                        rx.text('Ссылка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.input(
                            rx.input.slot(
                                rx.icon('user', size=17, color=rx.color('gray', 9))
                            ),
                            value=newLinkItem.tLink,
                            on_change=[newLinkItem.set_tLink, newLinkItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Ссылка',
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Иконка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.flex(
                            rx.match(
                                newLinkItem.tImage,
                                ("Ссылка", rx.icon("square-arrow-out-up-right")),
                                ("Сообщение", rx.icon("message-circle")),
                                ("Бот", rx.icon("bot")),
                                ("Наушники", rx.icon("headphones")),
                                ("Диск", rx.icon("disc")),
                                ("Картинка", rx.icon("image")),
                                ("Twitch", rx.icon("twitch")),
                                ("YouTube", rx.icon("youtube")),
                                ("Instagram", rx.icon("instagram")),
                                ("Dribbble", rx.icon("dribbble")),
                                ("Github", rx.icon("github")),
                                ("Стрелка вправо", rx.icon("circle-arrow-right")),
                            ),
                            rx.select(
                                [f"Ссылка", "Сообщение", "Бот", 'Наушники', 'Диск', 'Картинка', 'Twitch', 'YouTube', 'Instagram', 'Dribbble', 'Github', 'Стрелка вправо'],
                                width='250px',
                                default_value='Ссылка',
                                value=newLinkItem.tImage,
                                on_change=newLinkItem.set_tImage
                            ),
                            align='center',
                            direction='row',
                            spacing='2'
                        ),
                        width='100%',
                        direction='column',
                        spacing='2'
                    ),
                    margin_top='8px',
                    direction='row',
                    spacing='2'
                ),
                rx.divider(),
                rx.flex(
                    rx.flex(),
                    rx.flex(
                        rx.button('Очистить данные', variant='surface', color_scheme='blue', on_click=newLinkItem.onStart),
                        rx.dialog.close(rx.button('Изменить', disabled=newLinkItem.tButtonDisable, on_click=newLinkItem.editItem(item))),
                        direction='row',
                        align='center',
                        spacing='2'
                    ),
                    direction='row',
                    justify='between',
                    align='center',
                    spacing='2'
                ),
                spacing='2',
                direction='column'
            ),
            width='700px'
        ),
    )