
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.components.header as header
import profiler.components.newpage as newpage

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

from profiler.states.mypages import State

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@rx.page(route="/mypages", title="«Profiler» — Мои страницы", on_load=[LS.onLoad, State.onStart])
def index():
    return rx.cond(
            rx.State.is_hydrated,
            rx.container(
                header.index(),
                rx.card(
                    rx.flex(
                        rx.text('Мои страницы', font_family='SFProDisplayBold'),
                        newpage.index('2'),
                        justify='between',
                        align='center',
                    ),
                    rx.divider(margin_top='16px'),
                    rx.cond(
                        State.tCountPages == 0,
                        rx.flex(
                            rx.icon('circle-x', color=rx.color('tomato', 9), size=40),
                            rx.text('Нету страниц', font_family='SFProDisplayBold', size='5'),
                            rx.text('Создайте свою первую страницу', font_family='SFProDisplayMedium', size='2'),
                            direction='column',
                            align='center',
                            spacing='1',
                            margin_top='12px'
                        ),
                        rx.flex(
                            rx.foreach(State.tPages, lambda line:
                                       rx.flex(
                                           rx.foreach(line, lambda item:
                                               rx.menu.root(
                                                   rx.menu.trigger(
                                                       rx.card(
                                                           rx.flex(
                                                               rx.icon('file-text', size=20),
                                                               rx.flex(
                                                                   rx.text(item[16], font_family='SFProDisplayBold'),
                                                                   rx.flex(
                                                                       rx.icon('link', size=15, color=rx.color('gray', 8)),
                                                                       rx.cond(
                                                                           item[11] == '',
                                                                           rx.text('Отсутствует', font_family='SFProDisplayBold', color_scheme='gray'),
                                                                           rx.text(item[11], font_family='SFProDisplayBold', color_scheme='gray'),
                                                                       ),
                                                                       direction='row',
                                                                       spacing='1',
                                                                       align='center'
                                                                   ),
                                                                   direction='column',
                                                                   aling='center',
                                                               ),
                                                               direction='row',
                                                               align='center',
                                                               spacing='2'
                                                           ),
                                                           aling='center',
                                                           width='100%'
                                                       ),
                                                   ),
                                                   rx.menu.content(
                                                       rx.menu.item("Просмотр страницы", on_click=rx.redirect(f'/page/{item[0]}')),
                                                       rx.menu.item("Редактировать страницу", on_click=rx.redirect(f'/page/edit/{item[0]}')),
                                                   ),
                                               ),
                                            ),
                                           spacing='2',
                                           direction='row',
                                           width='100%'
                                       ),
                                       ),
                            direction='column',
                            align='center',
                            spacing='1',
                            margin_top='12px'
                        ),
                    ),
                    width='100%',
                    margin_top='12px',
                    size="2"
                ),
                size='4'
            ),
            rx.center(
                rx.spinner(),
                height="100vh",  # Высота экрана
            ),
    )