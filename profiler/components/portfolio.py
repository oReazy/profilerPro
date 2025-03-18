
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

    tPortfolio: list[list[str]]
    tPortfolioMassive: list[list[list[str]]]
    tPortfolioCount = 0
    iconColor = 'black'

    # --------------------------------------------------------


    async def onMousePortfolioIcon(self):
        self.iconColor = 'blue'


    async def unMousePortfolioIcon(self):
        self.iconColor = 'black'



    async def checkPage(self):
        args = self.router.page.params['id']
        PAGE = await database.getData('pages', 'id', f'"{args}"')
        self.tPortfolio = ast.literal_eval(PAGE[5])
        self.tPortfolioCount = len(self.tPortfolio)
        if self.tPortfolioCount > 0:
            massive = []
            line = []
            count = 0
            COLORS = []
            for NAME in self.tPortfolio:
                if count > 2:
                    massive.append(line)
                    count = 0
                    line = []
                    count = count + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], 'black']
                    line.append(MASSIVE_ITEM)
                else:
                    count = count + 1
                    MASSIVE_ITEM = [NAME[0], NAME[1], NAME[2], NAME[3], NAME[4], 'black']
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
                rx.foreach(State.tPortfolioMassive, lambda line:
                           rx.flex(
                               rx.foreach(line, lambda item:
                               rx.link(
                                   rx.card(
                                       rx.inset(
                                           rx.image(
                                               src=rx.get_upload_url(f'{item[4]}'),
                                               width="100%",
                                               height="120px",
                                               style=LS.style2
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
                                               rx.icon('square-arrow-out-up-right',)
                                           ),
                                           direction='row',
                                           align='center',
                                           justify='between'
                                       ),
                                       width='294.6px'
                                   ),
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