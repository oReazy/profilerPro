"""

[ PAGES ]

Главная страница проекта

"""
from idlelib.configdialog import font_sample_text

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

import profiler.components.header as header
import profiler.components.editName as editName
import profiler.components.portfolio as portfolio
from profiler.states.page import State as State

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

style = {"text-decoration": "none !important",  # Убираем подчёркивание
         "color": "inherit !important",  # Цвет наследуется от родителя
         "cursor": "hover",  # Убираем указатель на ссылке
        }
hover = {"color": "inherit !important",  # Цвет не меняется при наведении
        "text-decoration": "none !important",  # Подчёркивание не появляется
        "background-color": "transparent !important",  # Чтобы исключить изменения фона
        }
style2 = {
            "object-fit": "cover",  # Покрытие всей области
            "object-position": "center",  # Центровка изображения
         }

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@rx.page(route="/page/[id]/", title="«Profiler» — Профиль", on_load=[LS.onLoad, State.checkPage])
def index():
    return rx.container(
        rx.cond(
            rx.State.is_hydrated,
            rx.flex(
                rx.cond(
                    State.tErrorVisible == False,
                    rx.flex(
                        rx.flex(
                            rx.cond(
                                (State.tImages[1] == '/images/pages/wallpaper.png') | (State.tImages[1] == '/images/pages/wallpaper_alt.png'),
                                rx.center(rx.image(State.tImages[1], width='900px', height='160px', border_radius='12px')),
                                rx.center(rx.image(rx.get_upload_url(f'{State.tImages[1]}'), style=LS.style2, width='900px', height='160px', border_radius='12px')),
                            ),
                            rx.cond(
                                (State.tImages[1] == '/images/pages/wallpaper.png') | (State.tImages[1] == '/images/pages/wallpaper_alt.png'),
                                rx.center(rx.image(State.tImages[0], width='140px', height='140px', margin_top='-100px', margin_left='-721px', border="4px solid #FFFFFF", border_radius='12px',)),
                                rx.center(rx.image(rx.get_upload_url(f'{State.tImages[0]}'), style=LS.style2,width='140px', height='140px', margin_top='-100px', margin_left='-721px', border="4px solid #FFFFFF", border_radius='12px',)),
                            ),
                            rx.tabs.root(
                                rx.cond(
                                    State.tVision[4],
                                    rx.tabs.list(
                                        rx.tabs.trigger("Главная", value="tab1", font_family='SFProDisplayBold'),
                                        margin_left='278px',
                                        margin_top='-52px',
                                        margin_bottom='12px',
                                        width='740px'
                                    ),
                                ),
                                rx.tabs.content(
                                    rx.flex(
                                        rx.cond(
                                           State.tVision[0],
                                            rx.flex(
                                                rx.flex(
                                                    rx.text(f"{State.tName} {State.tSurname}", font_family='SFProDisplayBold', size='5'),
                                                    rx.flex(
                                                        rx.foreach(
                                                            State.tIcons, lambda item:
                                                            rx.match(
                                                                item[2],
                                                                ("badge-check", rx.tooltip(rx.icon('badge-check'), content=item[3], delay_duration=0.01, font_family='SFProDisplayBold')),
                                                                ("folder-code", rx.tooltip(rx.icon('folder-code'), content=item[3], delay_duration=0.01, font_family='SFProDisplayBold')),
                                                                ("bug", rx.tooltip(rx.icon('bug'), content=item[3], delay_duration=0.01, font_family='SFProDisplayBold')),
                                                                ("check-blue", rx.tooltip(rx.icon('check', color=rx.color('blue', 9), stroke_width=3), content=item[3], delay_duration=0.01, font_family='SFProDisplayBold')),
                                                            ),
                                                        ),
                                                        direction='row',
                                                        margin_left='5px',
                                                        spacing='2',
                                                    ),
                                                    align='center',
                                                    width='700px',
                                                    # margin_top='12px'
                                                ),
                                                rx.text(State.tAbout, font_family='SFProDisplayMedium'),
                                                direction='column',
                                                spacing='1'
                                            ),
                                            ),
                                        ),
                                    rx.cond(
                                        State.tVision[1] == True,
                                        rx.cond(
                                            State.tPortfolioCount == 1,
                                            rx.flex(
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[0][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[0][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[0][4]}'),
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
                                                                rx.text(State.tPortfolio[0][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[0][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[0], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(0),
                                                    on_mouse_leave=State.unMousePortfolio(0),
                                                    on_click=State.unMousePortfolio(0),
                                                    href=State.tPortfolio[0][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                margin_top='8px',
                                                direction='row',
                                                spacing='2'
                                            ),
                                        ),
                                    ),
                                    rx.cond(
                                        State.tVision[1] == True,
                                        rx.cond(
                                            State.tPortfolioCount == 2,
                                            rx.flex(
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[0][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[0][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[0][4]}'),
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
                                                                rx.text(State.tPortfolio[0][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[0][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[0], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(0),
                                                    on_mouse_leave=State.unMousePortfolio(0),
                                                    on_click=State.unMousePortfolio(0),
                                                    href=State.tPortfolio[0][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[1][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[1][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[1][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[1][4]}'),
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
                                                                rx.text(State.tPortfolio[1][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[1][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[1], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(1),
                                                    on_mouse_leave=State.unMousePortfolio(1),
                                                    on_click=State.unMousePortfolio(0),
                                                    href=State.tPortfolio[1][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                margin_top='8px',
                                                direction='row',
                                                spacing='2'
                                            ),
                                        ),
                                    ),
                                    rx.cond(
                                        State.tVision[1] == True,
                                        rx.cond(
                                            State.tPortfolioCount == 3,
                                            rx.flex(
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[0][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[0][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[0][4]}'),
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
                                                                rx.text(State.tPortfolio[0][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[0][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[0], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(0),
                                                    on_mouse_leave=State.unMousePortfolio(0),
                                                    on_click=State.unMousePortfolio(0),
                                                    href=State.tPortfolio[0][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[1][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[1][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[1][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[1][4]}'),
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
                                                                rx.text(State.tPortfolio[1][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[1][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[1], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(1),
                                                    on_mouse_leave=State.unMousePortfolio(1),
                                                    on_click=State.unMousePortfolio(1),
                                                    href=State.tPortfolio[1][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[2][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[2][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[2][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[2][4]}'),
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
                                                                rx.text(State.tPortfolio[2][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[2][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[2], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='294.6px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(2),
                                                    on_mouse_leave=State.unMousePortfolio(2),
                                                    on_click=State.unMousePortfolio(2),
                                                    href=State.tPortfolio[2][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                margin_top='8px',
                                                direction='row',
                                                spacing='2'
                                            ),
                                        ),
                                    ),
                                    rx.cond(
                                        State.tVision[1] == True,
                                        rx.cond(
                                            State.tPortfolioCount > 3,
                                            rx.flex(
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[0][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[0][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[0][4]}'),
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
                                                                rx.text(State.tPortfolio[0][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[0][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[0], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='276px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(0),
                                                    on_mouse_leave=State.unMousePortfolio(0),
                                                    on_click=State.unMousePortfolio(0),
                                                    href=State.tPortfolio[0][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[1][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[1][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[1][4]}'),
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
                                                                rx.text(State.tPortfolio[1][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[1][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[1], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='276px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(1),
                                                    on_mouse_leave=State.unMousePortfolio(1),
                                                    on_click=State.unMousePortfolio(1),
                                                    href=State.tPortfolio[1][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                rx.link(
                                                    rx.card(
                                                        rx.inset(
                                                            rx.cond(
                                                                (State.tPortfolio[2][4] == '/images/pages/portfolio120.png') | (State.tPortfolio[2][4] == '/images/pages/portfolio120_alt.png'),
                                                                rx.image(
                                                                    src=State.tPortfolio[0][4],
                                                                    width="100%",
                                                                    height="120px",
                                                                    style=LS.style2
                                                                ),
                                                                rx.image(
                                                                    src=rx.get_upload_url(f'{State.tPortfolio[2][4]}'),
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
                                                                rx.text(State.tPortfolio[2][1], font_family='SFProDisplayBold'),
                                                                rx.text(State.tPortfolio[2][2], font_family='SFProDisplayMedium', size='2', color_scheme='gray'),
                                                                direction='column',
                                                            ),
                                                            rx.flex(
                                                                rx.icon('square-arrow-out-up-right', color=rx.color(State.tPortfolioColors[2], 9))
                                                            ),
                                                            direction='row',
                                                            align='center',
                                                            justify='between'
                                                        ),
                                                        width='276px'
                                                    ),
                                                    on_mouse_enter=State.onMousePortfolio(2),
                                                    on_mouse_leave=State.unMousePortfolio(2),
                                                    on_click=State.unMousePortfolio(2),
                                                    href=State.tPortfolio[2][3],
                                                    style=LS.hover,
                                                    is_external=True
                                                ),
                                                portfolio.index(),
                                                margin_top='8px',
                                                direction='row',
                                                spacing='2',
                                            ),
                                        ),
                                    ),
                                    value="tab1",
                                    width='900px',
                                    margin_left='117px',
                                ),
                                rx.tabs.content(
                                    rx.text("item on tab 2", font_family='SFProDisplayBold'),
                                    value="tab2",
                                    margin_left='117px',
                                ),
                                default_value="tab1",
                                orientation="horizontal",
                            ),
                            direction='column',
                            spacing='2',
                            margin_top='60px'
                        ),
                        spacing='2',
                        direction='column'
                    ),
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.center(
                                    rx.icon('circle-x', color=rx.color('tomato', 9), size=40),
                                ),
                                rx.center(
                                    rx.text('Ошибка', font_family='SFProDisplayBold', size='5'),
                                ),
                                rx.center(
                                    rx.text(State.tErrorText, font_family='SFProDisplayMedium', margin_bottom='16px', size='2'),
                                ),
                                direction='column',
                                spacing='1'
                            ),
                            width='100%'
                        ),
                        margin_top='12px'
                    ),
                ),
                direction='column'
            ),
            rx.center(
                rx.spinner(),
                height="100vh",  # Высота экрана
            )
        ),
        size='4'
    )