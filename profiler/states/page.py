
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
from rxconfig import config
import ast

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class State(LS):
    tPage = ()
    tImages = []
    tErrorVisible = False
    tErrorText = ''
    tIcons: list[str]

    tName = ''
    tSurname = ''
    tAbout = ''
    tVision: list[bool, bool, bool, bool, bool]
    tPrivate = 1

    # --------------------------------------------------------

    tPortfolioColors = ['black', 'black', 'black', 'black', 'black']

    # --------------------------------------------------------

    async def onMousePortfolio(self, index):
        self.tPortfolioColors[index] = 'blue'


    async def unMousePortfolio(self, index):
        self.tPortfolioColors[index] = 'black'






    async def checkPageUrl(self):
        args = self.router.page.params['url']
        count = await database.getDataMultiCount('pages', 'url', f'"{args}"')
        if count > 0:
            self.tErrorVisible = False
            PAGE = await database.getData('pages', 'url', f'"{args}"')
            self.tPage = PAGE
            self.tImages = ast.literal_eval(PAGE[10])
            self.tName = PAGE[1]
            self.tSurname = PAGE[2]
            self.tAbout = PAGE[4]
            self.tPrivate = PAGE[12]
            self.tVision = ast.literal_eval(PAGE[17])
            self.tPortfolio = ast.literal_eval(PAGE[5])
            self.tPortfolioCount = len(self.tPortfolio)
            self.tPortfolioColors = ['black', 'black', 'black', 'black', 'black']

            if self.tPrivate == 1:
                self.tErrorVisible = True
                self.tErrorText = 'Страница закрыта настройками приватности'
            # ------------
            # Получение массива иконок
            self.tIcons = []
            iconsID = ast.literal_eval(PAGE[9])
            for item in iconsID:
                icon_info = await database.getData('icons', 'id', f"'{item}'")
                self.tIcons.append(icon_info)
            # ------------
        else:
            self.tErrorVisible = True
            self.tErrorText = 'Страницы не существует'

    async def checkPage(self):
        args = self.router.page.params['id']
        count = await database.getDataMultiCount('pages', 'id', f'"{args}"')
        if count > 0:
            self.tErrorVisible = False
            PAGE = await database.getData('pages', 'id', f'"{args}"')
            self.tPage = PAGE
            self.tImages = ast.literal_eval(PAGE[10])
            self.tName = PAGE[1]
            self.tSurname = PAGE[2]
            self.tAbout = PAGE[4]
            self.tPrivate = PAGE[12]
            self.tVision = ast.literal_eval(PAGE[17])
            self.tPortfolio = ast.literal_eval(PAGE[5])
            self.tPortfolioCount = len(self.tPortfolio)

            # ------------
            # Получение массива иконок
            self.tIcons = []
            iconsID = ast.literal_eval(PAGE[9])
            for item in iconsID:
                icon_info = await database.getData('icons', 'id', f"'{item}'")
                self.tIcons.append(icon_info)

            if self.tPrivate == 1:
                self.tErrorVisible = True
                self.tErrorText = 'Страница закрыта настройками приватности'
            # ------------
        else:
            self.tErrorVisible = True
            self.tErrorText = 'Страницы не существует'