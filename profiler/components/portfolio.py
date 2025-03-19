
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
from rxconfig import config
import ast

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

class State(LS):
    # --------------------------------------------------------

    tPortfolioMassive: list[list[list[str]]]
    iconColor = 'black'

    # --------------------------------------------------------


    async def onMousePortfolioIcon(self):
        self.iconColor = 'blue'


    async def unMousePortfolioIcon(self):
        self.iconColor = 'black'


    async def onMousePortfolio(self, index):
        target_element = index
        LINE = 0
        ITEM = 0
        for i, sublist in enumerate(self.tPortfolioMassive):
            for j, item in enumerate(sublist):
                if target_element in item:
                    LINE = i
                    ITEM = j
        self.tPortfolioMassive[LINE][ITEM][6] = 'blue'

    async def unMousePortfolio(self, index):
        target_element = index
        LINE = 0
        ITEM = 0
        for i, sublist in enumerate(self.tPortfolioMassive):
            for j, item in enumerate(sublist):
                if target_element in item:
                    LINE = i
                    ITEM = j
        self.tPortfolioMassive[LINE][ITEM][6] = 'black'

    async def checkPage(self):
        try:
            args = self.router.page.params['id']
            PAGE = await database.getData('pages', 'id', f'"{args}"')
        except:
            args = self.router.page.params['url']
            PAGE = await database.getData('pages', 'url', f'"{args}"')
        self.tPortfolio = ast.literal_eval(PAGE[5])
        self.tPortfolioCount = len(self.tPortfolio)
        if self.tPortfolioCount > 0:
            massive = []
            line = []
            count = 0
            COLOR_COUNT = -1
            for NAME in self.tPortfolio:
                if count > 2:
                    massive.append(line)
                    count = 0
                    line = []
                    count = count + 1
                    COLOR_COUNT = COLOR_COUNT + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], COLOR_COUNT, 'black']
                    line.append(MASSIVE_ITEM)
                else:
                    count = count + 1
                    COLOR_COUNT = COLOR_COUNT + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], COLOR_COUNT, 'black']
                    line.append(MASSIVE_ITEM)
            massive.append(line)
            self.tPortfolioMassive = massive

def index():
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.link(
                rx.card(
                    rx.flex(
                        rx.icon('circle-arrow-right', size=25, margin_left='-1px', margin_top='69.5px', margin_bottom='69.5px', color=rx.color(State.iconColor, 9)),
                        height='100%'
                    ),
                    height='100%',
                ),
                on_mouse_enter=State.onMousePortfolioIcon,
                on_mouse_leave=State.unMousePortfolioIcon,
                on_click=[State.checkPage, State.unMousePortfolioIcon],
                style=LS.hover,
                height='100%',
            ),
        ),
        rx.dialog.content(
            rx.flex(
                rx.flex(
                    rx.flex(
                        rx.image('/icons/icons8-full_image.svg', width='25px'),
                        rx.text('Портфолио', font_family='SFProDisplayBold', size='3'),
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
                rx.foreach(State.tPortfolioMassive, lambda line:
                           rx.flex(
                               rx.foreach(line, lambda item:
                               rx.link(
                                   rx.card(
                                       rx.inset(
                                           rx.cond(
                                               (item[4] == '/images/pages/portfolio120.png') | (item[4] == '/images/pages/portfolio120_alt.png'),
                                               rx.image(
                                                   src=item[4],
                                                   width="100%",
                                                   height="120px",
                                                   style=LS.style2
                                               ),
                                               rx.image(
                                                   src=rx.get_upload_url(f'{item[4]}'),
                                                   width="100%",
                                                   height="120px",
                                                   style=LS.style2
                                               ),
                                           ),
                                           side="top",
                                           decoding='cover',
                                           pb="current",
                                       ),
                                       rx.flex(
                                           rx.flex(
                                               rx.text(item[1], font_family='SFProDisplayBold'),
                                               rx.text(item[2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                               direction='column',
                                           ),
                                           rx.flex(
                                               rx.icon('square-arrow-out-up-right', color=rx.color(item[6], 9))
                                           ),
                                           direction='row',
                                           align='center',
                                           justify='between'
                                       ),
                                       width='294.6px'
                                   ),
                                   on_mouse_enter=State.onMousePortfolio(item[5]),
                                   on_mouse_leave=State.unMousePortfolio(item[5]),
                                   on_click=State.unMousePortfolio(item[5]),
                                   href=item[3],
                                   style=LS.hover,
                                   is_external=True
                               ),
                                          ),
                               direction='row',
                               spacing='2'
                           ),
                ),
                direction='column',
                spacing='2',
            ),
            style={
                "overflow": "hidden",
                "max_width": "950px"
            },
        ),
    )