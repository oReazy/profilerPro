
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
from rxconfig import config
import ast, pathlib

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class State(LS):
    tPage = ()
    tImages = []
    tErrorVisible = False
    tErrorText = ''

    tNamePage = ''
    tName = ''
    tSurname = ''
    tAbout = ''
    tUrl = ''
    tVision1 = False
    tVision2 = False
    tVision3 = False
    tVision4 = False
    tVision5 = False
    tPrivate = ''

    @rx.event
    async def handle_upload_wallpaper(self, files: list[rx.UploadFile]):
        # Указываем путь к папке TEST
        args = self.router.page.params['id']
        upload_dir = pathlib.Path(f"uploaded_files/{args}")

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
            self.tImages[1] = f'/{args}/{file.filename}'
            args = self.router.page.params['id']
            await database.setData('pages', 'id', f"'{args}'", 'images', f'\"{self.tImages}\"')
            self.USER = await database.getUserHash(f"'{self.HASH}'")

    @rx.event
    async def handle_upload_avatar2(self, files: list[rx.UploadFile]):
        # Указываем путь к папке TEST
        args = self.router.page.params['id']
        upload_dir = pathlib.Path(f"uploaded_files/{args}")

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

    @rx.event
    async def handle_upload_avatar(
            self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            args = self.router.page.params['id']
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.tImages[0] = file.filename
            args = self.router.page.params['id']
            await database.setData('pages', 'id', f"'{args}'", 'images', f'\"{self.tImages}\"')
            self.USER = await database.getUserHash(f"'{self.HASH}'")

    @rx.event
    async def handle_upload(
            self, files: list[rx.UploadFile]):
        for file in files:
            args = self.router.page.params['id']
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.tImages[1] = file.filename
            args = self.router.page.params['id']
            await database.setData('pages', 'id', f"'{args}'", 'images', f'\"{self.tImages}\"')
            self.USER = await database.getUserHash(f"'{self.HASH}'")

    async def unMouseAvatar(self):
        if self.tImages[0] == '/images/pages/avatar_alt.png':
            self.tImages[0] = '/images/pages/avatar.png'

    async def onMouseAvatar(self):
        if self.tImages[0] == '/images/pages/avatar.png':
            self.tImages[0] = '/images/pages/avatar_alt.png'

    async def unMouseWallpaper(self):
        if self.tImages[1] == '/images/pages/wallpaper_alt.png':
            self.tImages[1] = '/images/pages/wallpaper.png'

    async def onMouseWallpaper(self):
        if self.tImages[1] == '/images/pages/wallpaper.png':
            self.tImages[1] = '/images/pages/wallpaper_alt.png'

    async def deletePage(self):
        args = self.router.page.params['id']
        await database.deleteData('pages', 'id', f"'{args}'")
        return [rx.redirect('/mypages')]

    async def save(self):
        args = self.router.page.params['id']
        vision = [self.tVision1, self.tVision2, self.tVision3, self.tVision4, self.tVision5]
        private = 0
        if self.tPrivate == 'Открыта':
            private = 0
        else:
            private = 1;
        await database.setDataMulti('pages', 'id', f"'{args}'", f"name = '{self.tName}', surname = '{self.tSurname}', description = '{self.tAbout}', vision = \"{vision}\", private = '{private}', namePage = '{self.tNamePage}'")
        countUrls = await database.getDataMultiCount('pages', 'url', f"'{self.tUrl}'")
        if countUrls == 0:
            await database.setData('pages', 'id', f"'{args}'", 'url', f"'{self.tUrl}'")
        else:
            page_info = await database.getData('pages', 'url', f"'{self.tUrl}'")
            if int(page_info[0]) == int(args):
                pass
            else:
                if self.tUrl == '':
                    await database.setData('pages', 'id', f"'{args}'", 'url', f"''")
                else:
                    return rx.toast.error("Данная ссылка уже занята, попробуйте другую")

    async def checkPage(self):
        args = self.router.page.params['id']
        count = await database.getDataMultiCount('pages', 'id', f'"{args}"')
        if count > 0:
            PAGE = await database.getData('pages', 'id', f'"{args}"')
            if PAGE[14] == self.USER[0]:
                self.tErrorVisible = False
                self.tErrorText = ''
                self.tPage = PAGE
                self.tImages = ast.literal_eval(PAGE[10])
                self.tNamePage = PAGE[16]
                self.tName = PAGE[1]
                self.tSurname = PAGE[2]
                self.tAbout = PAGE[4]
                self.tUrl = PAGE[11]
                VISION = ast.literal_eval(PAGE[17])
                self.tVision1 = VISION[0]
                self.tVision2 = VISION[1]
                self.tVision3 = VISION[2]
                self.tVision4 = VISION[3]
                self.tVision5 = VISION[4]
                self.tPortfolio = ast.literal_eval(PAGE[5])
                self.tPortfolioCount = len(self.tPortfolio)
                self.tLinks = ast.literal_eval(PAGE[7])
                self.tLinksCount = len(self.tLinks)
                if int(PAGE[12]) == 1:
                    self.tPrivate = 'Закрыта'
                else:
                    self.tPrivate = 'Открыта'
            else:
                self.tErrorVisible = True
                self.tErrorText = 'У вас нету доступа к редактированию страницы'
        else:
            self.tErrorVisible = True
            self.tErrorText = 'Страницы не существует'