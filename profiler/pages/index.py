
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import reflex as rx
import json, ast, datetime, time

from rxconfig import config

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.database as database
from profiler.states.localStorage import Storage as LS

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

import profiler.components.header as header
import profiler.components.auth as auth
import profiler.components.registration as registration

# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————

@rx.page(route="/", title="«Profiler» — Главная страница", on_load=LS.onLoadLite)
def index():
    return rx.cond(
            rx.State.is_hydrated,
            rx.container(
                header.index(),
                rx.flex(
                    rx.image(
                        src="/images/index/portfolioHeader.jpg",
                        width="900px",
                        height="160px",
                        style=LS.style2,
                        border_radius='12px'
                    ),
                    rx.image(
                        src="/images/index/portfolioPhoto.jpg",
                        width="140px",
                        height="140px",
                        style=LS.style2,
                        border_radius='12px',
                        margin_top='-100px',
                        margin_left='-721px',
                        border="4px solid #FFFFFF",
                    ),
                    rx.text('Это ваше портфолио,', font_family='SFProTextBold', size='9', padding_top='25px'),
                    rx.text('которое привлечет всех.', font_family='SFProTextBold', size='9'),
                    rx.cond(
                        LS.HASH == '0',
                        rx.flex(
                            auth.index('3'),
                            registration.index('3'),
                            direction='row',
                            spacing='2',
                            margin_top='26px',
                        ),
                        rx.flex(
                            rx.button("Мои страницы", font_family='SFProDisplayBold', size='3', on_click=rx.redirect('/mypages')),
                            direction='row',
                            spacing='2',
                            margin_top='26px',
                        ),
                    ),
                    direction='column',
                    align='center',
                    padding_top='100px'
                ),
                rx.flex(
                    rx.text('Подробнее 🔽', font_family='SFProTextBold', size='3', margin_top='350px', margin_bottom='25px'),
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon.png', width='35px'),
                                    rx.text('Кастомизация', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Вы можете изменять как угодно вашу страницу. Доступно множество вариаций блоков для того, чтобы сделать вашу страницу особенной', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon2.png', width='35px'),
                                    rx.text('Ваша собственная ссылка', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Намного приятнее делиться собственной ссылкой с друзьями и коллегами. После создания вашей страницы, вам будет дана возможность изменить ее', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon3.png', width='35px'),
                                    rx.text('Портфолио', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Сервис предоставляет возможность делиться работами из разных площадок: Behance, YouTube, Vimeo, Dribbble и других площадок', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        spacing='2',
                        width='100%',
                        direction='row',
                    ),
                    rx.flex(
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon4.png', width='35px'),
                                    rx.text('Компании', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Ваше резюме могут смотреть компании, а также вы можете наблюдать за своими избранными компаниями и быть в курсе всех событий', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon5.png', width='35px'),
                                    rx.text('Делитесь страницей', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Сервис никак вас неограничивает в распространении вашей страницы. Делитесь ею везде: на сайтах с вакансиями, в соц. сетях', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        rx.card(
                            rx.flex(
                                rx.flex(
                                    rx.image('/icons/index/icon6.png', width='35px'),
                                    rx.text('Цены', font_family='SFProTextBold', size='3'),
                                    direction='row',
                                    spacing='2',
                                    align='center'
                                ),
                                rx.text('Мы стараемся для всех пользователей сделать сервис бесплатным, однако за дополнительную плату можно убрать рекламу с вашей страницы', font_family='SFProTextBold', size='2', color_scheme='gray'),
                                direction='column',
                                spacing='2'
                            ),
                            width='100%'
                        ),
                        spacing='2',
                        width='100%',
                        direction='row',
                    ),
                    spacing='2',
                    align='center',
                    direction='column'
                ),
                size='4'
            ),
            rx.center(
                rx.spinner(),
                height="100vh",  # Высота экрана
            ),
    )