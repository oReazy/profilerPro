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

class newPortfolioItem(LS):
    tName = ''
    tTitle = ''
    tDescription = ''
    tLink = ''
    tIndex = 0


    tButtonDisable = True
    tButtonLoading = False

    tErrorVision = False
    tErrorText = ''
    tImage = '/images/pages/portfolio120.png'


    async def delete(self, item):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        tPortfolio = list(tPortfolio)
        index = tPortfolio.index(item)
        tPortfolio.pop(index)
        await database.setData('pages', 'id', f"'{args}'", 'portfolio', f'\"{tPortfolio}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        self.tPortfolio = list(tPortfolio)


    async def onStart(self):
        self.tName = ''
        self.tTitle = ''
        self.tDescription = ''
        self.tLink = ''
        self.tImage = '/images/pages/portfolio120.png'
        self.tButtonDisable = True
        self.tButtonLoading = False
        self.tErrorVision = False
        self.tErrorText = ''

    async def loadItem(self, item):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        tPortfolio = list(tPortfolio)
        self.tIndex = tPortfolio.index(item)
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
        tPortfolio = ast.literal_eval(PAGE[5])
        tPortfolio = list(tPortfolio)
        tPortfolio[self.tIndex] = [self.tName, self.tTitle, self.tDescription, self.tLink, self.tImage]
        await database.setData('pages', 'id', f"'{args}'", 'portfolio', f'\"{tPortfolio}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        self.tPortfolio = list(tPortfolio)

    async def createItem(self):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        tPortfolio = list(tPortfolio)
        tPortfolio.append([self.tName, self.tTitle, self.tDescription, self.tLink, self.tImage])
        await database.setData('pages', 'id', f"'{args}'", 'portfolio', f'\"{tPortfolio}\"')
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        tPortfolio = ast.literal_eval(PAGE[5])
        self.tPortfolio = list(tPortfolio)



    async def checkForm(self):
        if self.tName != '' and self.tTitle != '' and self.tDescription != '' and self.tLink != '':
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
            self.tImage = f'/{args}/portfolio{file.filename[1:]}'

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

def index():
    return rx.dialog.root(
        rx.dialog.trigger(rx.button('Добавить работу', font_family='SFProDisplayBold', size='1', on_click=newPortfolioItem.onStart)),
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
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=newPortfolioItem.tName,
                    on_change=[newPortfolioItem.set_tName, newPortfolioItem.checkForm],
                    font_family='SFProDisplayBold',
                    placeholder='Название вашей работы (видно только вам)',
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
                            value=newPortfolioItem.tTitle,
                            on_change=[newPortfolioItem.set_tTitle, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Заголовок вашей работы',
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
                            value=newPortfolioItem.tDescription,
                            on_change=[newPortfolioItem.set_tDescription, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Напишите краткое описание',
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
                            value=newPortfolioItem.tLink,
                            on_change=[newPortfolioItem.set_tLink, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Ссылка на вашу работу',
                        ),
                        width='262px',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Картинка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.cond(
                            (newPortfolioItem.tImage == '/images/pages/portfolio120.png') | (newPortfolioItem.tImage == '/images/pages/portfolio120_alt.png'),
                            rx.upload(rx.center(rx.image(newPortfolioItem.tImage, width='282px', height='120px', border_radius='12px', on_mouse_enter=newPortfolioItem.onMouseImage, on_mouse_leave=newPortfolioItem.unMouseImgae)), id="upload_image", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=newPortfolioItem.handle_upload_portfolio(rx.upload_files(upload_id="upload_image")), padding='-40px', margin_left='0px', margin_right='0px', border='1px'),
                            rx.upload(rx.center(rx.image(rx.get_upload_url(f'{newPortfolioItem.tImage}'), style=LS.style2, width='282px', height='120px', border_radius='12px', on_mouse_enter=newPortfolioItem.onMouseImage, on_mouse_leave=newPortfolioItem.unMouseImgae)), id="upload_image", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=newPortfolioItem.handle_upload_portfolio(rx.upload_files(upload_id="upload_image")), padding='-40px', margin_left='0px', margin_right='0px', border='1px'),
                        ),
                        width='282px',
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
                        rx.button('Очистить данные', variant='surface', color_scheme='blue', on_click=newPortfolioItem.onStart),
                        rx.dialog.close(rx.button('Добавить', disabled=newPortfolioItem.tButtonDisable, on_click=newPortfolioItem.createItem)),
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
                    rx.image('/images/pages/icons8-image_file.svg', width='20px'),
                    rx.text(item[0], font_family='SFProDisplayBold'),
                    spacing='2',
                    direction='row',
                    align='center'
                ),
                width='800px',
                style=LS.hover,
                on_click=[newPortfolioItem.loadItem(item)]
            ),
        ),
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
                rx.input(
                    rx.input.slot(
                        rx.icon('user', size=17, color=rx.color('gray', 9))
                    ),
                    value=newPortfolioItem.tName,
                    on_change=[newPortfolioItem.set_tName, newPortfolioItem.checkForm],
                    font_family='SFProDisplayBold',
                    placeholder='Название вашей работы (видно только вам)',
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
                            value=newPortfolioItem.tTitle,
                            on_change=[newPortfolioItem.set_tTitle, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Заголовок вашей работы',
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
                            value=newPortfolioItem.tDescription,
                            on_change=[newPortfolioItem.set_tDescription, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Напишите краткое описание',
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
                            value=newPortfolioItem.tLink,
                            on_change=[newPortfolioItem.set_tLink, newPortfolioItem.checkForm],
                            font_family='SFProDisplayBold',
                            placeholder='Ссылка на вашу работу',
                        ),
                        width='262px',
                        direction='column',
                        spacing='2'
                    ),
                    rx.flex(
                        rx.text('Картинка', font_family='SFProDisplayBold', color_scheme='gray', size='2'),
                        rx.cond(
                            (newPortfolioItem.tImage == '/images/pages/portfolio120.png') | (newPortfolioItem.tImage == '/images/pages/portfolio120_alt.png'),
                            rx.upload(rx.center(rx.image(newPortfolioItem.tImage, width='282px', height='120px', border_radius='12px', on_mouse_enter=newPortfolioItem.onMouseImage, on_mouse_leave=newPortfolioItem.unMouseImgae)), id="upload_image", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=newPortfolioItem.handle_upload_portfolio(rx.upload_files(upload_id="upload_image")), padding='-40px', margin_left='0px', margin_right='0px', border='1px'),
                            rx.upload(rx.center(rx.image(rx.get_upload_url(f'{newPortfolioItem.tImage}'), style=LS.style2, width='282px', height='120px', border_radius='12px', on_mouse_enter=newPortfolioItem.onMouseImage, on_mouse_leave=newPortfolioItem.unMouseImgae)), id="upload_image", max_files=1, max_size=10000000, accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]}, on_drop=newPortfolioItem.handle_upload_portfolio(rx.upload_files(upload_id="upload_image")), padding='-40px', margin_left='0px', margin_right='0px', border='1px'),
                        ),
                        width='282px',
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
                        rx.button('Очистить данные', variant='surface', color_scheme='blue', on_click=newPortfolioItem.onStart),
                        rx.dialog.close(rx.button('Изменить', disabled=newPortfolioItem.tButtonDisable, on_click=newPortfolioItem.editItem)),
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